from pathlib import Path

from src.core.logger import get_logger
from src.yolo.detector import YOLODetector
from src.yolo.parser import parse_results
from src.yolo.exporter import save_detections

logger = get_logger("yolo")


IMAGE_DIR = Path("data/raw/images")


def run_inference():

    detector = YOLODetector()

    rows = []

    image_extensions = {".jpg", ".jpeg", ".png"}

    for image_path in IMAGE_DIR.rglob("*"):

        if image_path.suffix.lower() not in image_extensions:
            continue

        logger.info(f"Processing {image_path.name}")

        try:

            results = detector.predict(str(image_path))

            detections = parse_results(results)

            for detection in detections:

                detection["image"] = image_path.name
                detection["channel"] = image_path.parent.name

                rows.append(detection)

        except Exception:

            logger.exception(f"Failed on {image_path}")

    output = save_detections(rows)

    logger.info(f"Saved detections to {output}")
