# Automated Data Pipeline

> A production-grade Python pipeline that fetches data from a public API, cleans and processes it, computes KPI metrics, and exports a daily Markdown report — automatically. Built by [Code Alchemist Labs](https://codealchemistlabs.com).

---

## What This Does

This pipeline runs on a schedule (or on demand) and:

1. **Fetches** structured data from a configurable REST API endpoint
2. **Cleans** the response — handles missing values, type coercion, deduplication
3. **Computes KPIs** — counts, averages, trends, and custom business metrics
4. **Exports** a Markdown report + CSV snapshot to the `outputs/` directory
5. **Logs** every step with structured logging for debugging and auditing

**Real-world use cases:**
- Pull daily lead or sales data from a CRM API and generate a morning report
- Monitor API health and data quality over time
- Feed cleaned data into a downstream ML pipeline
- Automate client-facing reporting from raw API data

---

## Project Structure

```
automated-data-pipeline/
├── pipeline/
│   ├── __init__.py
│   ├── fetcher.py        # API data fetching with retries
│   ├── cleaner.py        # Data cleaning and normalization
│   ├── metrics.py        # KPI computation
│   └── reporter.py       # Markdown + CSV report writer
├── outputs/              # Generated reports and data snapshots (git-ignored)
├── main.py               # CLI entrypoint
├── config.py             # Config via environment variables
├── requirements.txt
├── .env.example
└── README.md
```

---

## Quickstart

```bash
# 1. Clone and install
git clone https://github.com/silverlining1/automated-data-pipeline.git
cd automated-data-pipeline
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env with your API endpoint and settings

# 3. Run the pipeline
python main.py

# 4. Check outputs/
# → outputs/report_2026-04-15.md
# → outputs/data_2026-04-15.csv
```

---

## Configuration

All settings are managed via environment variables in `.env`:

```env
API_URL=https://jsonplaceholder.typicode.com/posts
API_TIMEOUT=10
RETRY_ATTEMPTS=3
RETRY_BACKOFF=2
OUTPUT_DIR=outputs
LOG_LEVEL=INFO
```

---

## Retry Logic

The fetcher uses exponential backoff with configurable retries. If the API returns a 5xx error or times out, it automatically retries up to `RETRY_ATTEMPTS` times with an increasing wait between each attempt. This makes the pipeline reliable in production environments.

---

## Scheduling

To run daily, add a cron job:

```bash
# Run at 6:00 AM every day
0 6 * * * /usr/bin/python3 /path/to/automated-data-pipeline/main.py >> /var/log/pipeline.log 2>&1
```

Or use a cloud scheduler (AWS EventBridge, GCP Cloud Scheduler, etc.) pointing to the script.

---

## Tech Stack

- **Python 3.10+**
- **requests** — HTTP client with retry support
- **pandas** — data cleaning and transformation
- **python-dotenv** — config management
- **logging** — structured runtime logs

---

## Part of the Code Alchemist Labs Python Portfolio

| # | Project | Focus |
|---|---|---|
| 1 | [EDA Toolkit](https://github.com/silverlining1/EDAexample) | Data cleaning + analysis |
| 2 | [ML Pipeline](https://github.com/silverlining1/ml-pipeline) | scikit-learn model training + evaluation |
| 3 | **Automated Data Pipeline** (this) | API ingestion + reporting |
| 4 | [Prediction API](https://github.com/silverlining1/prediction-api) | FastAPI ML serving |

---

*Built by Earnest M. Walker · [Code Alchemist Labs](https://codealchemistlabs.com)*
