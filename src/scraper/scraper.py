"""
Telegram scraping functionality.

This module handles:
- Scraping messages from Telegram channels
- Downloading images
- Saving raw JSON data
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from telethon.errors import (
    ChannelPrivateError,
    FloodWaitError,
    UsernameInvalidError,
)
from telethon.tl.types import MessageMediaPhoto

from src.core.config import IMAGE_DIR, MESSAGE_DIR
from src.core.logger import get_logger
from src.scraper.client import authenticate, get_client
from src.utils.channels import CHANNELS
from src.utils.helpers import clean_filename

logger = get_logger("scraper")


def save_messages(messages: list[dict[str, Any]], channel_name: str) -> None:
    """
    Save scraped messages as raw JSON.

    Directory structure:
    data/raw/telegram_messages/YYYY-MM-DD/channel_name_HHMMSS.json
    """

    safe_channel = clean_filename(channel_name)

    today = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H%M%S")

    output_dir = MESSAGE_DIR / today
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{safe_channel}_{current_time}.json"

    try:
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(
                messages,
                file,
                ensure_ascii=False,
                indent=4,
            )

        logger.info(
            "Saved %d messages to %s",
            len(messages),
            output_file,
        )

    except Exception:
        logger.exception(
            "Failed to save messages for channel '%s'.",
            channel_name,
        )


async def download_image(
    client,
    message,
    channel_name: str,
) -> str | None:
    """
    Download an image from a Telegram message.

    Returns:
        Path to the downloaded image or None.
    """

    if not isinstance(message.media, MessageMediaPhoto):
        return None

    safe_channel = clean_filename(channel_name)

    channel_dir = IMAGE_DIR / safe_channel
    channel_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    image_path = channel_dir / f"{message.id}.jpg"

    try:
        await client.download_media(
            message,
            file=image_path,
        )

        logger.info(
            "Downloaded image for message %s",
            message.id,
        )

        return str(image_path)

    except Exception:
        logger.exception(
            "Failed downloading image for message %s",
            message.id,
        )

        return None


async def process_message(
    client,
    message,
    channel_name: str,
) -> dict[str, Any]:
    """
    Convert a Telegram message into a serializable dictionary.
    """

    image_path = None
 
    if not message:
        return None
    
    if not message.message and not message.media:
        return None
    
    if message.message and len(message.message.strip()) == 0:
        return None

    if message.media:
        image_path = await download_image(
            client,
            message,
            channel_name,
        )

    return {
        "message_id": message.id,
        "channel_name": channel_name,
        "message_date": (
            message.date.isoformat()
            if message.date
            else None
        ),
        "message_text": message.message or "",
        "has_media": message.media is not None,
        "image_path": image_path,
        "views": message.views or 0,
        "forwards": message.forwards or 0,
    }


async def scrape_channel(
    client,
    channel_name: str,
) -> None:
    """
    Scrape all messages from a Telegram channel.
    """

    logger.info("Starting scrape for channel '%s'.", channel_name)

    messages = []
    seen_ids = set()

    try:
        async for message in client.iter_messages(channel_name):

            if message.id in seen_ids:
                continue

            seen_ids.add(message.id)

            processed_message = await process_message(
                client,
                message,
                channel_name,
            )

            if processed_message is None:
                continue

            messages.append(processed_message)

        save_messages(messages, channel_name)

        logger.info(
            "Completed scraping '%s'. Total messages: %d",
            channel_name,
            len(messages),
        )

    except FloodWaitError as error:
        logger.error(
            "Telegram rate limit reached. Wait %d seconds.",
            error.seconds,
        )

    except ChannelPrivateError:
        logger.error(
            "Channel '%s' is private.",
            channel_name,
        )

    except UsernameInvalidError:
        logger.error(
            "Channel '%s' does not exist.",
            channel_name,
        )

    except Exception:
        logger.exception(
            "Unexpected error while scraping '%s'.",
            channel_name,
        )


async def scrape_all_channels() -> None:
    """
    Authenticate and scrape all configured Telegram channels.
    """

    client = get_client()

    try:
        await authenticate(client)

        logger.info("Telegram authentication successful.")
        logger.info("Channels loaded: %s", CHANNELS)

        for channel in CHANNELS:
            logger.info("Scraping channel: %s", channel)
            await scrape_channel(
                client,
                channel,
            )

    except Exception:
        logger.exception("Pipeline failed.")

    finally:
        await client.disconnect()
        logger.info("Disconnected from Telegram.")
