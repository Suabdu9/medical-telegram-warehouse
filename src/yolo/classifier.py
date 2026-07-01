PRODUCT_CLASSES = {
    "bottle",
    "cup",
    "bowl",
}


def classify_image(detected_classes):
    """
    Classify an image based on the detected object classes.

    Rules:
    - promotional: person + product
    - product_display: product only
    - lifestyle: person only
    - other: neither
    """

    classes = set(detected_classes)

    has_person = "person" in classes
    has_product = any(c in PRODUCT_CLASSES for c in classes)

    if has_person and has_product:
        return "promotional"

    if has_product:
        return "product_display"

    if has_person:
        return "lifestyle"

    return "other"
