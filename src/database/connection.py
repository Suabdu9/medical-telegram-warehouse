import psycopg2
from src.core.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


def get_connection():
    """
    Create PostgreSQL connection for the Telegram warehouse.
    """

    try:
        conn = psycopg2.connect(
            host="127.0.0.1",   # force IPv4 (Docker-safe)
            port=int(DB_PORT),
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        return conn

    except Exception as e:
        raise RuntimeError(f"Database connection failed: {e}")
    