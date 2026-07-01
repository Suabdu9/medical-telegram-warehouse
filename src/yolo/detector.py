from ultralytics import YOLO
from src.core.logger import get_logger

logger = get_logger("yolo")


class YOLODetector:
    """
    Loads and manages the YOLOv8 model.
    """

    def __init__(self, model_name="yolov8n.pt"):
        try:
            logger.info(f"Loading YOLO model: {model_name}")
            self.model = YOLO(model_name)
            logger.info("YOLO model loaded successfully.")

        except Exception as e:
            logger.exception("Failed to load YOLO model.")
            raise RuntimeError(e)

    def predict(self, image_path):
        """
        Run inference on a single image.
        """
        return self.model(image_path)
