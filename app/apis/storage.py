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

        try:
            old_status = self.get(f'card_{unique_token}')
        except self.NotFound:
            self.set_expire(f'card_{unique_token}', '', expiry)
            old_status = ''

        if new_status == 'RETAINED':
            if old_status =='ADDED':
                return True, 'Card already added but re-retained.'
            elif old_status == 'RETAINED':
                return True, 'Card alread retained but re-retained'
            else:
                self.set_expire(f'card_{unique_token}', new_status, expiry)
                return True, 'Card retained'

        elif new_status == 'ADDED':
            if old_status in ['RETAINED', 'DELETED']:
                self.set_expire(f'card_{unique_token}', new_status, expiry)
                return True, 'Card successfully added.'
            elif old_status == new_status:
                return False, 'Card cannot be added again.'
            else:
                return False, 'Card cannot be added - not yet retained.'

        elif new_status == 'DELETED':
            if old_status == 'ADDED':
                self.set_expire(f'card_{unique_token}', new_status, expiry)
                return True, 'Card successfully deleted.'
            elif old_status in ['RETAINED', 'DELETED']:
                return False, f'Card cannot be deleted. Card is not added.'
            else:
                return False, 'Card cannot be added - not yet retained.'
