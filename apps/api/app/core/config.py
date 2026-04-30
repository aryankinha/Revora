import os
from pathlib import Path
from dotenv import load_dotenv

# Robustly find the .env file relative to this file's location
# Path: revora/apps/api/app/core/config.py -> parents[2] is revora/apps/api/
BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)


class Settings:
    PROJECT_NAME: str = "Revora API"

    # Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # DATABASE
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # FRONTEND
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    # CORS
    CORS_ORIGINS: list[str] = [
        o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()
    ]
    CORS_ALLOW_CREDENTIALS: bool = os.getenv("CORS_ALLOW_CREDENTIALS", "false").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }

    # Google Credentials
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI: str = os.getenv(
        "GOOGLE_REDIRECT_URI", "http://localhost:8000/gmail/callback"
    )
    GOOGLE_SSO_REDIRECT_URI: str = os.getenv(
        "GOOGLE_SSO_REDIRECT_URI", "http://localhost:8000/auth/google/callback"
    )

    # LEAD GENERATION
    HUNTER_API_KEY: str = os.getenv("HUNTER_API_KEY")
    APOLLO_API_KEY: str = os.getenv("APOLLO_API_KEY")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")


settings = Settings()
