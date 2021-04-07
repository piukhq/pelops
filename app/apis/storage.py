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
                added: (True, 'Card already added but re-retained.'),
                retained: (True, 'Card already retained but re-retained'),
                deleted: (True, 'Card retained'),
                '': (True, 'Card retained')
            }

            success, message = actions[old_status]
            if success:
                self.set_expire(f'card_{unique_token}', new_status, expiry)

        elif new_status == added:
            actions = {
                added: (False, 'Card cannot be re-added.'),
                retained: (True, 'Card added successfully'),
                deleted: (False, 'Card not retained'),
                '': (False, 'Card not retained')
            }
            success, message = actions[old_status]
            if success:
                self.set_expire(f'card_{unique_token}', new_status, expiry)

        elif new_status == deleted:
            actions = {
                added: (True, 'Card deleted successfully.'),
                retained: (False, 'Card not yet added'),
                deleted: (False, 'Card already deleted'),
                '': (False, 'Card not yet added')
            }
            success, message = actions[old_status]
            if success:
                self.set_expire(f'card_{unique_token}', new_status, expiry)

        return success, message
