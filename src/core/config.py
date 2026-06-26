from pathlib import Path

from dotenv import load_dotenv
import os

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
IMAGE_DIR = RAW_DIR / "images"
MESSAGE_DIR = RAW_DIR / "telegram_messages"

LOG_DIR = PROJECT_ROOT / "logs"

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def validate_config() -> None:
    """Validate required environment variables."""

    required = {
        "API_ID": API_ID,
        "API_HASH": API_HASH,
        "PHONE_NUMBER": PHONE_NUMBER,
    }

    missing = [key for key, value in required.items() if not value]

    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}"
        )


validate_config()

for directory in (
    DATA_DIR,
    RAW_DIR,
    IMAGE_DIR,
    MESSAGE_DIR,
    LOG_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)
