import logging
import os
from functools import lru_cache

from pydantic import AnyUrl, BaseSettings, AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = os.getenv("TESTING", 0)
    database_url: AnyUrl = os.environ.get("DATABASE_URL")
    # secret_key: str = os.environ.get("SECRET_KEY")
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SECRET_KEY: str

# settings = Settings()


@lru_cache()
def get_settings() -> Settings:
    log.info("Loading config settings from the environment...")
    return Settings()
