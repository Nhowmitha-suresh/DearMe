from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = 'postgresql+asyncpg://user:password@localhost:5432/dearme'
    REDIS_URL: str = 'redis://localhost:6379/0'
    CHROMA_URL: str = 'http://localhost:8000'
    FIREBASE_PROJECT_ID: str | None = None
    SECRET_KEY: str = 'change-me'
    ALLOWED_HOSTS: str = '*'
    DEBUG: bool = False

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
