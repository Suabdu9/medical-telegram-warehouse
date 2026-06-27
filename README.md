# Medical Telegram Data Warehouse

An end-to-end data engineering project that collects data from Ethiopian medical Telegram channels, stores it in a PostgreSQL data warehouse, transforms it using dbt into a dimensional star schema, enriches image data with YOLO object detection, and exposes analytical insights through a FastAPI service.

> **Project Status:** 🚧 In Progress

---

## Overview

This project was developed as part of a Data Engineering challenge to build a modern ELT pipeline for analytical reporting.

The pipeline performs the following steps:

* Scrapes messages and images from public Ethiopian medical Telegram channels using Telethon.
* Stores raw data in a partitioned JSON data lake.
* Loads raw data into PostgreSQL.
* Transforms and cleans the data using dbt.
* Builds a dimensional star schema for analytics.
* Enriches image data using YOLOv8 object detection.
* Serves analytical reports through a FastAPI REST API.
* Orchestrates the complete pipeline using Dagster.

---

## Project Architecture

```text
Telegram Channels
        │
        ▼
Raw JSON Data Lake
        │
        ▼
PostgreSQL (Raw Schema)
        │
        ▼
dbt Staging Models
        │
        ▼
Star Schema
(Dimensions + Facts)
        │
        ▼
YOLO Image Enrichment
        │
        ▼
Analytical API (FastAPI)
        │
        ▼
Dagster Orchestration
```

---

## Technologies Used

* Python 3.13
* Telethon
* PostgreSQL
* Docker
* dbt
* FastAPI
* SQLAlchemy
* Dagster
* Ultralytics YOLOv8
* Git & GitHub

---

## Current Features

### Task 1

* Telegram authentication
* Multi-channel scraping
* JSON data lake
* Image downloading
* Logging
* Error handling

### Task 2

* PostgreSQL data warehouse
* Raw schema
* JSON loader
* dbt project
* Staging model
* Star schema
* Data quality tests
* Documentation

---

## Repository Structure

```text
medical-telegram-warehouse/

├── api/
├── data/
├── logs/
├── medical_warehouse/
├── notebooks/
├── scripts/
├── src/
├── tests/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Suabdu9/medical-telegram-warehouse.git
cd medical-telegram-warehouse
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it.

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Create a `.env` file

```env
API_ID=YOUR_API_ID
API_HASH=YOUR_API_HASH
PHONE_NUMBER=YOUR_PHONE_NUMBER

DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=telegram_db
DB_USER=postgres
DB_PASSWORD=postgres

LOG_LEVEL=INFO
```

---

### 5. Start PostgreSQL

```bash
docker compose up -d
```

Verify:

```bash
docker ps
```

---

### 6. Run the scraper

```bash
python -m scripts.run_scraper
```

---

### 7. Load raw data into PostgreSQL

```bash
python -m scripts.load_to_postgres
```

---

### 8. Run dbt

Check the connection:

```bash
dbt debug --project-dir medical_warehouse
```

Run the models:

```bash
dbt run --project-dir medical_warehouse
```

Run the tests:

```bash
dbt test --project-dir medical_warehouse
```

Generate documentation:

```bash
dbt docs generate --project-dir medical_warehouse
```

Serve documentation:

```bash
dbt docs serve --project-dir medical_warehouse --port 8081
```

---

## Data Warehouse

### Fact Table

* `fct_messages`

### Dimension Tables

* `dim_channels`
* `dim_dates`

---

## Data Source

Public Ethiopian Telegram channels, including:

* CheMed
* Lobelia Cosmetics
* Tikvah Pharma

---

## Future Work

* YOLOv8 image enrichment
* FastAPI analytical endpoints
* Dagster orchestration
* Dockerized deployment
* CI/CD with GitHub Actions

---

## Author

Sumeya Abdulsemed

Software Engineering Graduate | Cyber Incident Responder | Backend Development Enthusiast | Data Engineering & AI Student
