from typing import ClassVar, Literal
from zoneinfo import ZoneInfo

from bink_logging_utils import init_loguru_root_sink
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: ClassVar[bytes] = b"\xa2\xaeY9>\xda=;\xcc\x7f\x05\xf6\x94.\x93~\xb16\x8e%2\x01\x83\x10"
    DEV_HOST: str = "0.0.0.0"
    DEV_PORT: int = 5050
    DEBUG: bool = False

    JSON_LOGGING: bool = True
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "DEBUG"

    AUTH_USERNAME: str = "binktest"
    AUTH_PASSWORD: str = "9702u37553bvo89p9n2qnf9ow8bv9we8bn1oib6452v9"

    REDIS_PASSWORD: str = ""
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: str = "0"
    REDIS_PROTOCOL: str = "redis"
    REDIS_URL: str = f"{REDIS_PROTOCOL}://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

    TIMEZONE: str = "Europe/London"
    TZINFO: ClassVar[ZoneInfo] = ZoneInfo(TIMEZONE)

    class Config:
        case_sensitive = True
        # env var settings priority ie priority 1 will override priority 2:
        # 1 - env vars already loaded (ie the one passed in by kubernetes)
        # 2 - env vars read from .env file
        # 3 - values assigned directly in the Settings class
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


init_loguru_root_sink(
    json_logging=settings.JSON_LOGGING,
    sink_log_level=settings.LOG_LEVEL,
    show_pid=False,
)
