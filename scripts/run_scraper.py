import asyncio

from src.scraper.scraper import scrape_all_channels
from src.core.logger import get_logger

logger = get_logger("scraper")


async def main():

    try:
        await scrape_all_channels()
        logger.info("Scraping pipeline completed successfully.")

    except Exception as e:
        logger.exception(f"Pipeline failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
