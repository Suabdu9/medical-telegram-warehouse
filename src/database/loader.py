"""
Load raw Telegram JSON into PostgreSQL.
"""

import json
from pathlib import Path

from psycopg2.extras import execute_values

from src.core.logger import get_logger
from src.database.connection import get_connection
from src.database.schema import create_schema, create_table

logger = get_logger("database")


RAW_DATA_DIR = Path("data/raw/telegram_messages")


def get_json_files() -> list[Path]:
    """
    Return all JSON files recursively.
    """

    return sorted(RAW_DATA_DIR.rglob("*.json"))


def read_json(file_path: Path) -> list[dict]:
    """
    Read one JSON file.
    """

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_rows(records: list[dict]) -> list[tuple]:
    """
    Convert JSON records into tuples.
    """

    rows = []

    for record in records:

        rows.append(
            (
                record["message_id"],
                record["channel_name"],
                record["message_date"],
                record["message_text"],
                record["has_media"],
                record["image_path"],
                record["views"],
                record["forwards"],
            )
        )

    return rows


def insert_rows(conn, rows: list[tuple]) -> None:
    """
    Batch insert records.
    """

    sql = """
        INSERT INTO raw.telegram_messages (

            message_id,
            channel_name,
            message_date,
            message_text,
            has_media,
            image_path,
            views,
            forwards

        )
        VALUES %s

        ON CONFLICT (message_id)
        DO NOTHING;
    """

    with conn.cursor() as cursor:

        execute_values(
            cursor,
            sql,
            rows,
            page_size=500,
        )

    conn.commit()


def load_raw_data() -> None:
    """
    Load every JSON file into PostgreSQL.
    """

    conn = get_connection()

    try:

        create_schema(conn)
        create_table(conn)

        files = get_json_files()

        if not files:

            logger.warning("No JSON files found.")

            return

        total_rows = 0

        for file in files:

            logger.info("Loading %s", file.name)

            records = read_json(file)

            rows = build_rows(records)

            if rows:

                insert_rows(conn, rows)

                total_rows += len(rows)

        logger.info(
            "Successfully loaded %s records into PostgreSQL.",
            total_rows,
        )

    except Exception:

        conn.rollback()

        logger.exception("Failed loading raw data.")

        raise

    finally:

        conn.close()
