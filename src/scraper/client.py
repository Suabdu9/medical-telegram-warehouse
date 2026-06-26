from telethon import TelegramClient

from src.core.config import API_HASH, API_ID, PHONE_NUMBER


def get_client() -> TelegramClient:
    """
    Create and return a configured Telegram client.
    """

    return TelegramClient(
        session="telegram_session",
        api_id=int(API_ID),
        api_hash=API_HASH,
    )


async def authenticate(client: TelegramClient) -> None:
    """
    Authenticate the Telegram client.
    """

    await client.start(phone=PHONE_NUMBER)
