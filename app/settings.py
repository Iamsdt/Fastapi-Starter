from functools import lru_cache
from typing import Optional

from fastapi import Depends
from fastapi_mail import ConnectionConfig
from pydantic import BaseSettings

IS_PRODUCTION = False


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Starter"
    APP_VERSION: str = "1.0.0"
    debug: bool

    # Database
    POSTGRESQL_HOSTNAME: Optional[str]
    POSTGRESQL_USERNAME: Optional[str]
    POSTGRESQL_PASSWORD: Optional[str]
    POSTGRESQL_DATABASE: Optional[str]
    POSTGRESQL_PORT: Optional[str]

    # auth
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    APP_CLIENT_ID: str
    APP_CLIENT_SECRET: str

    # path
    BASE_URL: str = "/home/shudipto/projects/podcast/podcast_fastapi/"
    MEDIA_URL: str = "media/"

    # Email
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_TLS: bool
    MAIL_SSL: bool
    USE_CREDENTIALS: bool

    class Config:
        env_file = "app/utils/envs/debug.env"
        env_file_encoding = 'utf-8'
        allow_mutation = True


@lru_cache()
def get_settings() -> Settings:
    return Settings(_env_file='app/utils/envs/prod.env' if IS_PRODUCTION else 'app/utils/envs/debug.env')


@lru_cache()
def get_email_config(settings: Settings = Depends(get_settings)) -> ConnectionConfig:
    return ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_TLS=settings.MAIL_TLS,
        MAIL_SSL=settings.MAIL_SSL,
        USE_CREDENTIALS=settings.USE_CREDENTIALS
    )
