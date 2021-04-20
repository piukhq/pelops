import logging

from environment import env_var, read_env

SECRET_KEY = b"\xa2\xaeY9>\xda=;\xcc\x7f\x05\xf6\x94.\x93~\xb16\x8e%2\x01\x83\x10"

read_env()

DEV_HOST = env_var("DEV_HOST", "0.0.0.0")
DEV_PORT = env_var("DEV_PORT", "5050")
DEBUG = env_var("DEBUG", False)

AUTH_USERNAME = env_var("binktest", "")
AUTH_PASSWORD = env_var("987g8ovb293bv029b3nvp9083bv0p1bf1f0hg874vb8g62vi", "u37553bvo89p9n2qnf9ow8bv9we8bn1oib6452v9")

REDIS_PASSWORD = env_var("REDIS_PASSWORD", "")
REDIS_HOST = env_var("REDIS_HOST", "localhost")
REDIS_PORT = env_var("REDIS_PORT", "6379")
REDIS_DB = env_var("REDIS_DB", "0")
REDIS_PROTOCOL = env_var("REDIS_PROTOCOL", "redis")
REDIS_URL = env_var("REDIS_DSN", f"{REDIS_PROTOCOL}://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")


# Logging settings
logging.basicConfig(format="%(process)s %(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("pelops_logger")
logger.setLevel(logging.DEBUG)
