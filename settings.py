from environment import env_var, read_env


SECRET_KEY = b'\xa2\xaeY9>\xda=;\xcc\x7f\x05\xf6\x94.\x93~\xb16\x8e%2\x01\x83\x10'

read_env()

DEV_HOST = env_var("DEV_HOST", "0.0.0.0")
DEV_PORT = env_var("DEV_PORT", "5050")
