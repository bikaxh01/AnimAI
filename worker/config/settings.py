from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    OPENAI_API_KEY: str
    ENV: str = "PROD"
    API_BASE_URL: str = "http://localhost:8000/api/v1"
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_GROUP_NAME: str = "workers"
    REDIS_STREAM_NAME: str = "orders"
    REDIS_PASSWORD: str = ""
settings = Settings()
