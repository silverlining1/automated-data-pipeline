# Automated Data Pipeline

> A production-style Python pipeline that fetches 7-day weather forecast data from the [Open-Meteo](https://open-meteo.com/) free API, cleans it, computes daily KPIs, and writes a Markdown report + CSV snapshot — all with retry logic and structured logging. Built by [Code Alchemist Labs](https://codealchemistlabs.com).

**Days 21–25 of the Code Alchemist Labs 30-Day Python Portfolio.**

---

## What It Does

1. **Fetches** daily weather forecast (temp, precipitation, wind, condition) from Open-Meteo — no API key required
2. **Cleans** the nested JSON response into a flat, typed DataFrame
3. **Computes KPIs**: avg highs/lows, total precipitation, rainy day count, wind peaks, sky condition breakdown
4. **Writes outputs**: a Markdown report and a dated CSV snapshot to `outputs/`

Runs in under 5 seconds. Designed to be scheduled via cron.

---

## Project Structure

```
automated-data-pipeline/
├── pipeline/
│   ├── __init__.py
│   ├── fetcher.py      # HTTP client with retry + backoff
│   ├── cleaner.py      # JSON → DataFrame, type coercion, derived columns
│   ├── metrics.py      # KPI computation
│   └── reporter.py     # Markdown + CSV writer
├── outputs/            # Generated reports (git-ignored)
├── tests/
│   ├── test_fetcher.py
│   ├── test_cleaner.py
│   └── test_metrics.py
├── main.py             # CLI entrypoint
├── config.py           # Config via environment variables
├── requirements.txt
├── .env.example
└── README.md
```

---

## Quickstart

```bash
git clone https://github.com/silverlining1/automated-data-pipeline.git
cd automated-data-pipeline
pip install -r requirements.txt

# Copy and customize (optional — defaults to Atlanta, GA)
cp .env.example .env

# Run the pipeline
python main.py

# Check outputs/
# → outputs/report_YYYY-MM-DD.md
# → outputs/weather_YYYY-MM-DD.csv
```

---

## Configuration

```env
# Location
LATITUDE=33.749
LONGITUDE=-84.388
CITY_NAME=Atlanta, GA
FORECAST_DAYS=7

# API behavior
API_TIMEOUT=15
RETRY_ATTEMPTS=3
RETRY_BACKOFF=2.0

# Output
OUTPUT_DIR=outputs
LOG_LEVEL=INFO
```

---

## Scheduling (Optional)

Run daily at 6 AM using cron:

```bash
# crontab -e
0 6 * * * cd /path/to/automated-data-pipeline && python main.py
```

---

## Example Output

```markdown
# Weather Report — Atlanta, GA
Run date: 2026-04-15 | Generated: 2026-04-15 06:01:23

## Forecast Window
- From: 2026-04-15
- To:   2026-04-21
- Days covered: 7

## Temperature Summary
- Avg high: 72.4 °F
- Avg low: 54.1 °F

## Precipitation
- Total precipitation: 0.42 in
- Rainy days: 2

## Daily Detail
| Date       | High (°F) | Low (°F) | Precip (in) | Condition        |
|------------|-----------|----------|-------------|------------------|
| 2026-04-15 | 74.2      | 55.0     | 0.00        | Mainly clear     |
| 2026-04-16 | 68.1      | 52.3     | 0.21        | Moderate rain    |
```

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Tech Stack

- **requests** — HTTP client
- **pandas** — data cleaning and transformation
- **python-dotenv** — config management
- **pytest** — unit tests
- **logging** — structured runtime logs

---

## Part of the Code Alchemist Labs Python Portfolio

| # | Project | Focus |
|---|---|---|
| 1 | [EDA Toolkit](https://github.com/silverlining1/EDAexample) | Data cleaning + analysis |
| 2 | [ML Pipeline](https://github.com/silverlining1/ml-pipeline) | scikit-learn model training |
| 3 | **Automated Data Pipeline** (this) | API ingestion + reporting |
| 4 | [Prediction API](https://github.com/silverlining1/prediction-api) | FastAPI ML serving |

---

*Built by Earnest M. Walker · [Code Alchemist Labs](https://codealchemistlabs.com)*
