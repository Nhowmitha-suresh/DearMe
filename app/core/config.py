from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379/0"
    CHROMA_URL: str = "http://localhost:8000"
    FIREBASE_PROJECT_ID: str | None = None

    class Config:
        env_file = '.env'


settings = Settings()
from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = 'postgresql+asyncpg://user:password@localhost:5432/dearme'
    REDIS_URL: str = 'redis://localhost:6379/0'
    SECRET_KEY: str = 'change-me'
    ALLOWED_HOSTS: str = '*'

    class Config:
        env_file = '.env'


settings = Settings()
