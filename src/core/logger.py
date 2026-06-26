"""
Application-wide logging configuration.

This module provides reusable loggers for every component of the project.
"""

import logging
import logging.config
from datetime import datetime

from src.core.config import LOG_DIR, LOG_LEVEL

LOG_DIR.mkdir(parents=True, exist_ok=True)

GENERAL_LOG = LOG_DIR / f"{datetime.now():%Y-%m-%d}.log"
SCRAPER_LOG = LOG_DIR / "scraper.log"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": LOG_LEVEL.upper(),
        },
        "general_file": {
            "class": "logging.FileHandler",
            "filename": str(GENERAL_LOG),
            "formatter": "standard",
            "encoding": "utf-8",
            "level": LOG_LEVEL.upper(),
        },
        "scraper_file": {
            "class": "logging.FileHandler",
            "filename": str(SCRAPER_LOG),
            "formatter": "standard",
            "encoding": "utf-8",
            "level": LOG_LEVEL.upper(),
        },
    },
    "loggers": {
        "scraper": {
            "handlers": [
                "console",
                "general_file",
                "scraper_file",
            ],
            "level": LOG_LEVEL.upper(),
            "propagate": False,
        },
    },
    "root": {
        "handlers": [
            "console",
            "general_file",
        ],
        "level": LOG_LEVEL.upper(),
    },
}

logging.config.dictConfig(LOGGING_CONFIG)


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger.

    Use:
        get_logger("scraper")
        get_logger(__name__)
    """

    return logging.getLogger(name)
