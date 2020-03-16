from environment import env_var, read_env
import logging


SECRET_KEY = b'\xa2\xaeY9>\xda=;\xcc\x7f\x05\xf6\x94.\x93~\xb16\x8e%2\x01\x83\x10'

read_env()

DEV_HOST = env_var("DEV_HOST", "0.0.0.0")
DEV_PORT = env_var("DEV_PORT", "5050")
DEBUG = env_var("DEBUG", False)


REDIS_PASSWORD = env_var('REDIS_PASSWORD', '')
REDIS_HOST = env_var('REDIS_HOST', 'localhost')
REDIS_PORT = env_var('REDIS_PORT', '6379')
REDIS_DB = env_var('REDIS_DB', '0')
REDIS_PROTOCOL = env_var('REDIS_PROTOCOL', 'redis')
REDIS_URL = '{protocol}://:{password}@{host}:{port}/{db}'.format(**{
    'protocol': REDIS_PROTOCOL,
    'password': REDIS_PASSWORD,
    'host': REDIS_HOST,
    'port': REDIS_PORT,
    'db': REDIS_DB
})


# Logging settings
logging.basicConfig(format='%(process)s %(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger('pelops_logger')
logger.setLevel(logging.DEBUG)