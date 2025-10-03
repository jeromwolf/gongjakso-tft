"""
Application Configuration
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # App Info
    APP_NAME: str = "Gongjakso TFT API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://localhost/gongjakso_tft"

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://gongjakso-tft.up.railway.app"
    ]

    # AI Services
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None

    # Email
    RESEND_API_KEY: Optional[str] = None
    FROM_EMAIL: str = "noreply@gongjakso-tft.up.railway.app"

    # Newsletter
    NEWSLETTER_SCHEDULE: str = "0 9 * * *"  # Daily at 9 AM
    NEWSLETTER_ENABLED: bool = True

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
