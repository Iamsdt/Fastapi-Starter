from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings

IS_PRODUCTION = False


class Settings(BaseSettings):
    APP_NAME: str = "Podcast"
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

    class Config:
        env_file = "app/utils/envs/debug.env"
        env_file_encoding = 'utf-8'
        allow_mutation = False


@lru_cache()
def get_settings() -> Settings:
    return Settings(_env_file='app/utils/envs/prod.env' if IS_PRODUCTION else 'app/utils/envs/debug.env')
