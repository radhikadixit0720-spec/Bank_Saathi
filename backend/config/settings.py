"""
Centralised application settings.

All configuration is read from environment variables so that no secret
(database credentials, allowed origins, etc.) is ever hard-coded in source
control. Copy `backend/.env.example` to `backend/.env` and fill in real
values for local development or deployment.
"""
import os
from typing import List

try:
    # python-dotenv is optional at runtime (e.g. in some deploy environments
    # the platform injects real env vars directly) but is used for local dev.
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover - dotenv is in requirements.txt
    pass


def _split_origins(raw: str) -> List[str]:
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


class Settings:
    APP_NAME: str = "Bank Saathi API"
    APP_VERSION: str = "2.0.0"

    # --- Database -----------------------------------------------------
    MONGODB_URI: str = os.getenv("MONGODB_URI", "")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "bank_saathi")

    # --- CORS -----------------------------------------------------------
    ALLOWED_ORIGINS: List[str] = _split_origins(
        os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
    )

    # --- Optional AI provider for the Simple Language Assistant ---------
    # If not configured, a rule-based fallback simplifier is used instead
    # (see services/language_service.py). No key is required for the demo.
    AI_PROVIDER_API_KEY: str = os.getenv("AI_PROVIDER_API_KEY", "")
    AI_PROVIDER_MODEL: str = os.getenv("AI_PROVIDER_MODEL", "")

    # --- Misc -------------------------------------------------------------
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10"))


settings = Settings()
