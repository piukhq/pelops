from redis import StrictRedis


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

    def update(self, token, new_status):
        if new_status == 'RETAINED':
            self.set_expire(f'card_{token}', 'RETAINED', 6000)

        elif new_status == 'ADDED':
            old_status = self.get(f'card_{token}')
            if old_status == 'RETAINED' or old_status == 'DELETED':
                self.set_expire(f'card_{token}', 'ADDED', 6000)
                return True, 'Card successfully added'
            elif old_status == 'ADDED':
                return False, 'Card cannot be added again.'
            else:
                return False, 'Card cannot be added - not yet retained.'

        elif new_status == 'DELETED':
            old_status = self.get(f'card_{token}')
            if old_status == 'ADDED':
                self.set_expire(f'card_{token}', 'DELETED', 6000)
                return True, 'Card successfully deleted'
            elif old_status == 'RETAINED' or old_status == 'DELETED':
                return False, f'Card cannot be deleted. Card is currently {old_status}.'
            else:
                return False, 'Card cannot be added - not yet retained.'
