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

        status_retained = 'RETAINED'
        status_added = 'ADDED'
        status_deleted = 'DELETED'

        try:
            old_status = self.get(f'card_{unique_token}')
        except self.NotFound:
            self.set_expire(f'card_{unique_token}', '', expiry)
            old_status = ''

        if new_status == status_retained:
            self.set_expire(f'card_{unique_token}', new_status, expiry)
            success = True
            message = 'Card retained'

        elif new_status == status_added:
            if old_status in [status_retained, status_deleted]:
                self.set_expire(f'card_{unique_token}', new_status, expiry)
                success = True
                message = 'Card successfully added.'
            else:
                message = f'Card cannot be added. Card status is {old_status}'

        elif new_status == status_deleted:
            if old_status == status_added:
                self.set_expire(f'card_{unique_token}', new_status, expiry)
                success = True
                message = 'Card successfully deleted.'
            else:
                message = f'Card cannot be deleted. Card status {old_status}'

        return success, message
