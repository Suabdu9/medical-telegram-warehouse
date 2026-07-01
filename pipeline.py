from dagster import op, job, schedule, Definitions
import subprocess


@op
def scrape_telegram_data() -> bool:
    subprocess.run(
        ["python", "-m", "scripts.run_scraper"],
        check=True,
    )
    return True


@op
def load_raw_to_postgres(start: bool) -> bool:
    subprocess.run(
        ["python", "-m", "scripts.load_to_postgres"],
        check=True,
    )
    return True


@op
def run_yolo_enrichment(start: bool) -> bool:
    subprocess.run(
        ["python", "-m", "scripts.run_yolo"],
        check=True,
    )
    return True


@op
def load_detections(start: bool) -> bool:
    subprocess.run(
        ["python", "-m", "scripts.load_detections"],
        check=True,
    )
    return True


@op
def run_dbt_transformations(start: bool):
    subprocess.run(
        [
            "dbt",
            "run",
            "--project-dir",
            "medical_warehouse",
            "--full-refresh",
        ],
        check=True,
    )


@job
def medical_pipeline():
    a = scrape_telegram_data()
    b = load_raw_to_postgres(a)
    c = run_yolo_enrichment(b)
    d = load_detections(c)
    run_dbt_transformations(d)


@schedule(
    cron_schedule="0 0 * * *",
    job=medical_pipeline,
)
def daily_pipeline(_context):
    return {}


defs = Definitions(
    jobs=[medical_pipeline],
    schedules=[daily_pipeline],
)
