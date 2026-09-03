"""Application configuration settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    PROJECT_NAME: str = "CloudPhoneBook API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Database settings
    # Default to sqlite local file for easy development/testing without docker,
    # or postgresql+psycopg://postgres:postgres@localhost:5432/cloudphonebook in production/docker
    DATABASE_URL: str = "sqlite:///./cloudphonebook.db"

    # JWT Security settings
    JWT_SECRET_KEY: str = "dev-secret-key-cloudphonebook-change-in-production-1234567890"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # CORS
    CORS_ORIGINS: list[str] = ["*"]


settings = Settings()
