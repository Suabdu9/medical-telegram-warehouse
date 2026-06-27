"""
Database schema creation.
"""

from psycopg2.extensions import connection


def create_schema(conn: connection) -> None:
    """
    Create raw schema if it doesn't exist.
    """

    with conn.cursor() as cursor:

        cursor.execute(
            """
            CREATE SCHEMA IF NOT EXISTS raw;
            """
        )

    conn.commit()


def create_table(conn: connection) -> None:
    """
    Create telegram_messages table.
    """

    with conn.cursor() as cursor:

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS raw.telegram_messages (

                message_id BIGINT PRIMARY KEY,

                channel_name TEXT NOT NULL,

                message_date TIMESTAMP,

                message_text TEXT,

                has_media BOOLEAN,

                image_path TEXT,

                views INTEGER,

                forwards INTEGER,

                ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            );
            """
        )

    conn.commit()
