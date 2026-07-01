import pandas as pd
import psycopg2
from src.core.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from src.core.logger import get_logger

logger = get_logger("loader")

CSV_PATH = "data/processed/enriched_detections.csv"


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def load_detections():
    try:
        logger.info("Loading detections CSV...")

        df = pd.read_csv(CSV_PATH)

        conn = get_connection()
        cur = conn.cursor()

        inserted = 0

        for _, row in df.iterrows():

            cur.execute(
                """
                INSERT INTO image_detections (
                    message_id, image, channel, class_name, confidence,
                    x1, y1, x2, y2, image_category
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    int(row["message_id"]) if pd.notna(row["message_id"]) else None,
                    row["image"],
                    row["channel"],
                    row["class_name"],
                    row["confidence"],
                    row["x1"],
                    row["y1"],
                    row["x2"],
                    row["y2"],
                    row["image_category"],
                ),
            )

            inserted += 1

        conn.commit()

        cur.close()
        conn.close()

        logger.info(f"Inserted {inserted} detections into PostgreSQL")

    except Exception as e:
        logger.exception(f"Failed to load detections: {e}")
        raise


if __name__ == "__main__":
    load_detections()
