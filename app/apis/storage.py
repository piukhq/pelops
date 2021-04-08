from redis import StrictRedis
from settings import logger
from datetime import datetime


class Redis:
    class NotFound(Exception):
        pass

    def __init__(self, url):
        self.store = StrictRedis.from_url(url)

    @staticmethod
    def _key(key):
        return "pelops-{}".format(key)

    def set(self, key, value):
        self.store.set(self._key(key), value)

    def set_expire(self, key, value, expire=600):
        self.store.setex(self._key(key), expire, value)

    def get(self, key):
        val = self.store.get(self._key(key))
        if not val:
            raise self.NotFound
        return val.decode()

    def delete(self, key):
        self.store.delete(self._key(key))

    def update_if_per(self, psp_token, new_status):

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

        if psp_token[:3] == 'PER':
            expiry = 6000
            unique_token = psp_token[4:]
            success, message, err = self.update(unique_token, new_status, expiry)
            logger.info(f'Card persistence: {message}')
            try:
                log = self.get(f'cardlog_{unique_token}')
            except self.NotFound:
                log = ''
            now = datetime.now()
            log = log + f'{now}: {message}\n'
            self.set_expire(f'cardlog_{unique_token}', log, expiry)
            return True, success, message, err
        else:
            return False, False, '', {}

    def update(self, unique_token, new_status, expiry):

        success = False
        message = 'Failed'

        retained = 'RETAINED'
        added = 'ADDED'
        deleted = 'DELETED'

        try:
            old_status = self.get(f'card_{unique_token}')
        except self.NotFound:
            self.set_expire(f'card_{unique_token}', '', expiry)
            old_status = ''

        if new_status == retained:
            actions = {
                added: (False, True, f'Card {unique_token} re-retained (Currently ADDED).', None),
                retained: (False, True, f'Card {unique_token} re-retained (Currently RETAINED).', None),
                deleted: (False, True, f'Card {unique_token} re-retained (Currently DELETED).', None),
                '': (True, True, f'Card {unique_token} retained.', None)
            }

            change, success, message, err = actions[old_status]
            if change:
                self.set_expire(f'card_{unique_token}', new_status, expiry)

        elif new_status == added:
            actions = {
                added: (False, False, f'Card {unique_token} cannot be added - card already exists.',
                        {'amex': '', 'vop': 'RTMENRE0025'}),
                retained: (True, True, f'Card {unique_token} added successfully.', None),
                deleted: (True, True, f'Card {unique_token} re-added.', None),
                '': (False, False, f'Card {unique_token} not yet retained.', {'amex': '', 'vop': 'RTMENRE0021'})
            }
            change, success, message, err = actions[old_status]
            if change:
                self.set_expire(f'card_{unique_token}', new_status, expiry)

        elif new_status == deleted:
            actions = {
                added: (True, True, f'Card {unique_token} deleted successfully.', None),
                retained: (False, False, f'Card {unique_token} not yet added.', {'amex': '', 'vop': 'RTMENRE0050'}),
                deleted: (False, False, f'Card {unique_token} already deleted.', {'amex': '', 'vop': 'RTMENRE0026'}),
                '': (False, False, f'Card {unique_token} not yet added.', {'amex': '', 'vop': 'RTMENRE0026'})
            }
            change, success, message, err = actions[old_status]
            if change:
                self.set_expire(f'card_{unique_token}', new_status, expiry)

        return success, message, err
