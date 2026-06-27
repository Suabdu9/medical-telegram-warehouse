import os
from pathlib import Path
from dotenv import load_dotenv

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Load .env
ENV_PATH = BASE_DIR / ".env"

if not ENV_PATH.exists():
    raise FileNotFoundError(f".env file not found: {ENV_PATH}")

load_dotenv(ENV_PATH)

# -------------------------
# Telegram
# -------------------------
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

# -------------------------
# PostgreSQL
# -------------------------
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "telegram_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

# -------------------------
# Logging
# -------------------------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

print(f"[CONFIG] Loaded .env from: {ENV_PATH}")
