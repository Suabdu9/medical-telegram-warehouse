def parse_results(results):
    """
    Convert YOLO Results objects into dictionaries.
    """

    detections = []

    for result in results:

        for box in result.boxes:

            cls_id = int(box.cls.item())

            detections.append(
                {
                    "class_id": cls_id,
                    "class_name": result.names[cls_id],
                    "confidence": float(box.conf.item()),
                    "x1": float(box.xyxy[0][0]),
                    "y1": float(box.xyxy[0][1]),
                    "x2": float(box.xyxy[0][2]),
                    "y2": float(box.xyxy[0][3]),
                }
            )

    return detections
