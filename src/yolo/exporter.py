from pathlib import Path
import pandas as pd

OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_detections(rows):

    df = pd.DataFrame(rows)

    output = OUTPUT_DIR / "detections.csv"

    df.to_csv(output, index=False)

    return output
