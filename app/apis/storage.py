from redis import StrictRedis
from settings import logger
from datetime import datetime


class Redis:
    class NotFound(Exception):
        pass

    def __init__(self, url):
        self.store = StrictRedis.from_url(url)
        self.expiry = 6000

    @staticmethod
    def _key(key):
        return "pelops-{}".format(key)

    def set(self, key, value):
        self.store.set(self._key(key), value)

    def set_expire(self, key, value, expire=None):
        if expire is None:
            expire = self.expiry
        self.store.setex(self._key(key), expire, value)

    def append_to_rlist(self, key, value, expire=None):
        if expire is None:
            expire = self.expiry
        # Appends value to redis list and resets expiry
        self.store.rpush(key, value)
        self.store.expire(key, expire)

    def get(self, key):
        val = self.store.get(self._key(key))
        if not val:
            raise self.NotFound
        return val.decode()

    def delete(self, key):
        self.store.delete(self._key(key))

    def rlist_to_list(self, key):
        # Reads redis list and decodes elements to string
        list_bytes = self.store.lrange(key, 0, -1)
        list_decoded = [x.decode("utf-8") for x in list_bytes]
        return list_decoded

    def update_if_per(self, psp_token, new_status, token):

        """
        For Persistence (PER):

        The PER prefix, added to the psp_token, will simulate persistence in Redis, allowing Pelops to store the results
        of some calls (currently ADD, DEL and RET) in a cache for testing purposes. This will be reflected in the card
        'status', which is updated as successful call are made to simulate card status in 3rd party vaults/dbs.:
            e.g. PER_4423snv489os093

        Individual card status can be queried via the '/cardstatus' endpoint (without the PER prefix):
            e.g. {pelops url}/cardstatus/4423snv489os093

        The status of cards added/deleted etc. without the PER prefix will not be stored/updated.
        """

        if psp_token[:4] == 'PER_':

            success, log_message, err_code, err_message = self.update_status(psp_token, new_status, token, self.expiry)

            now = datetime.now()
            logger.info(f'Card Persistence: {log_message}')
            self.append_to_rlist(f'cardlog_{psp_token}', f'[{now}] {log_message}', self.expiry)

            return True, success, log_message, err_code, err_message
        else:
            return False, False, '', {}, ''

    def update_status(self, psp_token, new_status, token, expiry):
        # Checks logic for retain/add/delete to persistence layer and applies/rejects requested change as necessary.
        # Also returns error codes and messages for later use, if request fails logic.
        success = False
        log_message = 'Failed'
        err = None
        err_code = ''
        err_message = ''

        err_message_list = {
            'RCCMP005': 'Card Member already Synced for the Token - Duplicate request or malfunction in input request.',
            'RCCMU009': 'Invalid Token/Token not found.',
            'RTMENRE0025': 'The user key provided is already in use - duplicate card.',
            'RTMENRE0021': 'Invalid user status or user already enrolled',
            'RTMENRE0050': 'Invalid user status',
            'RTMENRE0026': 'Enroll User not found',
        }

        retained = 'RETAINED'
        added = 'ADDED'
        deleted = 'DELETED'

        try:
            old_status = self.get(f'card_{psp_token}')
        except self.NotFound:
            self.set_expire(f'card_{psp_token}', '', expiry)
            old_status = ''

        if new_status == retained:
            actions = {
                added: (False, True, f'Card {psp_token} re-retained (Currently ADDED).', None),
                retained: (False, True, f'Card {psp_token} re-retained (Currently RETAINED).', None),
                deleted: (False, True, f'Card {psp_token} re-retained (Currently DELETED).', None),
                '': (True, True, f'Card {psp_token} retained.', None)
            }

            change, success, log_message, err = actions[old_status]
            if change:
                self.set_expire(f'card_{psp_token}', new_status, expiry)

        elif new_status == added:
            actions = {
                added: (False, False, f'Card {psp_token} cannot be added - card already exists.',
                        {'amex': 'RCCMP005',
                         'visa': 'RTMENRE0025'}),
                retained: (True, True, f'Card {psp_token} added successfully.', None),
                deleted: (True, True, f'Card {psp_token} re-added.', None),
                '': (False, False, f'Card {psp_token} not yet retained.', {'amex': 'RCCMU009',
                                                                           'visa': 'RTMENRE0021'})
            }
            change, success, log_message, err = actions[old_status]
            if change:
                self.set_expire(f'card_{psp_token}', new_status, expiry)

        elif new_status == deleted:
            actions = {
                added: (True, True, f'Card {psp_token} deleted successfully.', None),
                retained: (False, False, f'Card {psp_token} not yet added.', {'amex': 'RCCMU009',
                                                                              'visa': 'RTMENRE0050'}),
                deleted: (False, False, f'Card {psp_token} already deleted.', {'amex': 'RCCMU009',
                                                                               'visa': 'RTMENRE0026'}),
                '': (False, False, f'Card {psp_token} not yet added.', {'amex': 'RCCMU009',
                                                                        'visa': 'RTMENRE0026'})
            }
            change, success, log_message, err = actions[old_status]
            if change:
                self.set_expire(f'card_{psp_token}', new_status, expiry)

        if err:
            err_code = err[token]
            err_message = err_message_list[err_code]
        return success, log_message, err_code, err_message

    def add_activation(self, psp_token, offer_id, activation_id):
        # If using the PER_ prefix (see above), activation records will be persistently stored and request
        # returned as successful, provided the associated psp_token has a status of 'ADDED' within Pelops'
        # persistence layer.

        now = datetime.now()
        if psp_token[:4] == 'PER_':
            try:
                status = self.get(f'card_{psp_token}')
            except self.NotFound:
                return False
            if status == 'ADDED':
                self.append_to_rlist(f'card_activations_{psp_token}', activation_id)
                self.append_to_rlist(f'cardlog_{psp_token}', f'[{now}] Activated card/scheme pair with VOP for scheme '
                                                             f'{offer_id}. Activation id: {activation_id}')
                logger.info(f'Card persistence: Activation {activation_id} created')
            else:
                self.append_to_rlist(f'cardlog_{psp_token}',
                                     f'[{now}] Activation failed for: {activation_id}. No added card found')
                logger.info(f'Card persistence: Activation {activation_id} failed. No added card found')
                return False
        return True

    def remove_activation(self, psp_token, activation_id):
        # If using the PER_ prefix (see above), deactivation records will be removed (as well as logged) and request
        # will return as successful, provided the associated psp_token has a status of 'ADDED' within Pelops'
        # persistence layer.

        now = datetime.now()
        if psp_token[:4] == 'PER_':
            try:
                status = self.get(f'card_{psp_token}')
            except self.NotFound:
                return False
            if status == 'ADDED':

                if self.store.lrem(f'card_activations_{psp_token}', -1, activation_id):
                    # lrem returns number of removed items, 0 if none found/removed
                    self.append_to_rlist(f'cardlog_{psp_token}', f'[{now}] Deactivated card/scheme pair. '
                                                                 f'Activation id: {activation_id}')
                    logger.info(f'Card persistence: Activation {activation_id} deactivated')
                else:
                    return False
            else:
                self.append_to_rlist(f'cardlog_{psp_token}', f'[{now}] Deactivation failed for activation_id '
                                                             f'{activation_id}. No added card found.')
                logger.info(f'Card persistence: Deactivation failed for activation_id {activation_id}. '
                            f'No added card found')
                return False
        return True
