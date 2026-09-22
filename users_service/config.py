import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "fast_api"
    DB_USER: str = "gorbanna"
    DB_PASSWORD: str = "my_super_password"


settings = Settings()

SECRET_KEY="secret_key"
ALGORITHM="HS256"


def get_db_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")