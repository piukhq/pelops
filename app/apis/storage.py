from redis import StrictRedis
from settings import logger


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
            success, message = self.update(psp_token[4:], new_status)
            logger.info(f'Card persistence: {message}')
        else:
            pass

    def update(self, unique_token, new_status):

        expiry = 6000
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
                added: (False, 'Card re-retained but still added.'),
                retained: (False, 'Card already retained but re-retained.'),
                deleted: (False, 'Card re-retained but still deleted.'),
                '': (True, 'Card retained.')
            }

            success, message = actions[old_status]
            if success:
                self.set_expire(f'card_{unique_token}', new_status, expiry)

        elif new_status == added:
            actions = {
                added: (False, 'Card cannot be re-added.'),
                retained: (True, 'Card added successfully.'),
                deleted: (False, 'Card not retained.'),
                '': (False, 'Card not retained.')
            }
            success, message = actions[old_status]
            if success:
                self.set_expire(f'card_{unique_token}', new_status, expiry)

        elif new_status == deleted:
            actions = {
                added: (True, 'Card deleted successfully.'),
                retained: (False, 'Card not yet added.'),
                deleted: (False, 'Card already deleted.'),
                '': (False, 'Card not yet added.')
            }
            success, message = actions[old_status]
            if success:
                self.set_expire(f'card_{unique_token}', new_status, expiry)

        return success, message
