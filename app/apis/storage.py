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
            if old_status == added:
                message = 'Card already added but re-retained.'
            elif old_status == retained:
                message = 'Card already retained but re-retained'
            elif old_status == '':
                self.set_expire(f'card_{unique_token}', new_status, expiry)
                message = 'Card retained'
            success = True

        elif new_status == added:
            if old_status == retained or old_status == deleted:
                self.set_expire(f'card_{unique_token}', new_status, expiry)
                success = True
                message = 'Card successfully added.'
            elif old_status == new_status:
                message = 'Card cannot be added again.'
            elif old_status == '':
                message = 'Card cannot be added - not yet retained.'

        elif new_status == deleted:
            if old_status == added:
                self.set_expire(f'card_{unique_token}', new_status, expiry)
                success = True
                message = 'Card successfully deleted.'
            elif old_status == retained or old_status == deleted:
                message = 'Card cannot be deleted. Card is not added.'
            elif old_status == '':
                message = 'Card cannot be added - not yet retained.'

        return success, message
