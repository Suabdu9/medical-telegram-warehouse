"""
Entry point for loading raw Telegram data into PostgreSQL.
"""

from src.database.loader import load_raw_data
from src.core.logger import get_logger

logger = get_logger("database")


def main():
    try:
        logger.info("Starting PostgreSQL loading pipeline...")
        load_raw_data()
        logger.info("Loading pipeline completed successfully.")

    except Exception as e:
        logger.exception("Pipeline failed: %s", e)
        raise


if __name__ == "__main__":
    main()
