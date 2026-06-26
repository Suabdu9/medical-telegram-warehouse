import json
import re
from pathlib import Path


def save_json(data: list, output_path: Path):

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4,
            default=str,
        )


def clean_filename(name: str) -> str:
    """
    Make a string safe for use as a file or folder name.
    """
    return re.sub(r'[<>:"/\\|?*]', "_", name.strip())
