import asyncio

from src.scraper.client import authenticate, get_client
from src.core.logger import logger


async def main():

    client = get_client()

    try:

        await authenticate(client)

        logger.info("Telegram authentication successful.")

    except Exception as e:

        logger.exception(f"Authentication failed: {e}")

    finally:

        await client.disconnect()


if __name__ == "__main__":

    asyncio.run(main())
