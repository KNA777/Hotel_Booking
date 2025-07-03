from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"] = None

    DB_USER: str = None
    DB_PASS: str = None
    DB_HOST: str = None
    DB_PORT: int = None
    DB_NAME: str = None

    JWT_SECRET_KEY: str = None
    JWT_ALGORITHM: str = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = None

    REDIS_HOST: str = None
    REDIS_PORT: int = None

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
