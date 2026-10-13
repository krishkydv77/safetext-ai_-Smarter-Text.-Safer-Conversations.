from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    REDIS_URL: str = "redis://localhost:6379"
    RATE_LIMIT: int = 30  # requests per minute per user

    class Config:
        env_file = ".env"

settings = Settings()
