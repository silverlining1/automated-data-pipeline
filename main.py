"""CLI entrypoint for the Automated Data Pipeline.

Fetches 7-day weather forecast from Open-Meteo (free, no API key),
cleans it, computes KPIs, and writes a Markdown report + CSV snapshot.

Usage:
    python main.py
    python main.py --output results/
    python main.py --city "Atlanta, GA"

Cron example (daily at 6am):
    0 6 * * * cd /path/to/project && python main.py
"""

import argparse
import logging
import os
import sys
from datetime import date

import config
from pipeline.fetcher import fetch_data
from pipeline.cleaner import clean_data
from pipeline.metrics import compute_metrics
from pipeline.reporter import write_report

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("pipeline.main")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Automated Data Pipeline — Code Alchemist Labs",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--output", default=config.OUTPUT_DIR, help="Output directory")
    parser.add_argument("--city", default=config.CITY_NAME, help="City name label for report")
    return parser.parse_args()


def main():
    args = parse_args()
    today = str(date.today())
    os.makedirs(args.output, exist_ok=True)

    logger.info("=" * 55)
    logger.info(f"Pipeline run: {today}  |  City: {args.city}")
    logger.info(f"API: {config.API_URL[:70]}...")

    # Step 1: Fetch
    raw_data = fetch_data(
        config.API_URL,
        timeout=config.API_TIMEOUT,
        retries=config.RETRY_ATTEMPTS,
        backoff=config.RETRY_BACKOFF,
    )
    if raw_data is None:
        logger.error("Data fetch failed after all retries. Exiting.")
        sys.exit(1)

    # Step 2: Clean
    df = clean_data(raw_data)
    if df.empty:
        logger.error("No data remaining after cleaning. Exiting.")
        sys.exit(1)

    # Step 3: Compute KPIs
    metrics = compute_metrics(df)

    # Step 4: Write report
    report_path = write_report(df, metrics, today, args.output, city=args.city)

    logger.info(f"Pipeline complete. Report: {report_path}")
    print(f"\n✅ Done! Report → {report_path}")


if __name__ == "__main__":
    main()
