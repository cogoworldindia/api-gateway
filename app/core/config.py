from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_PORT: int = 8000
    REDIS_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    REFRESH_TOKEN_REDIS_PREFIX: str = "refresh_token:"
    AUTH_SERVICE_URL: str
    EMAIL_SERVICE_URL: str
    USER_SERVICE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
