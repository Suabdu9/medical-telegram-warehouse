from pathlib import Path
import re

import pandas as pd

from src.core.logger import get_logger
from src.yolo.classifier import classify_image

logger = get_logger("yolo")

INPUT_FILE = Path("data/processed/detections.csv")
OUTPUT_FILE = Path("data/processed/enriched_detections.csv")


def extract_message_id(filename):
    """
    Extract Telegram message_id from filenames like:
    """

    try:
        return int(Path(filename).stem)
    except ValueError:
        return None


def enrich_detections():

    logger.info("Loading detections.csv...")

    df = pd.read_csv(INPUT_FILE)

    df["message_id"] = df["image"].apply(extract_message_id)

    image_categories = {}

    for image_name, group in df.groupby("image"):

        detected_classes = group["class_name"].tolist()

        image_categories[image_name] = classify_image(detected_classes)

    df["image_category"] = df["image"].map(image_categories)

    columns = [
        "message_id",
        "image",
        "channel",
        "class_name",
        "confidence",
        "x1",
        "y1",
        "x2",
        "y2",
        "image_category",
    ]

    df = df[columns]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    logger.info(f"Saved enriched detections to {OUTPUT_FILE}")
