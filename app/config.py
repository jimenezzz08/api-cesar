# from pydantic import BaseSettings
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"
        extra = "allow"


class SettingsAlembic(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        extra = "allow"


settings_alembic = SettingsAlembic()
settings = Settings()
