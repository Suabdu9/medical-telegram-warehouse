import logging
import logging.config
from datetime import datetime

from src.core.config import LOG_DIR, LOG_LEVEL

# Ensure log directory exists
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / f"{datetime.now():%Y-%m-%d}.log"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": LOG_LEVEL.upper(),
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": str(LOG_FILE),
            "formatter": "standard",
            "encoding": "utf-8",
            "level": LOG_LEVEL.upper(),
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": LOG_LEVEL.upper(),
    },
}

logging.config.dictConfig(LOGGING_CONFIG)


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger instance.

    Args:
        name (str): Usually __name__ from the calling module.

    Returns:
        logging.Logger: Configured logger.
    """
    return logging.getLogger(name)
