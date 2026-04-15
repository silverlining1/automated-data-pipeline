"""Data cleaning and normalization for API responses."""

import logging
import pandas as pd

logger = logging.getLogger(__name__)


def clean_data(raw_data: list | dict) -> pd.DataFrame:
    """Convert raw API response into a clean, analysis-ready DataFrame.

    Args:
        raw_data: JSON response from the API (list of records or single dict).

    Returns:
        Cleaned pandas DataFrame.
    """
    if isinstance(raw_data, dict):
        raw_data = [raw_data]

    df = pd.DataFrame(raw_data)
    initial_rows = len(df)
    logger.info(f"Raw data: {initial_rows:,} rows, {len(df.columns)} columns")

    # Strip whitespace from all string columns
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda col: col.str.strip() if col.dtype == "object" else col)

    # Drop fully empty rows
    df = df.dropna(how="all")

    # Drop duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    dupes = before - len(df)
    if dupes:
        logger.info(f"Removed {dupes:,} duplicate rows")

    df = df.reset_index(drop=True)
    logger.info(f"Cleaned data: {len(df):,} rows (removed {initial_rows - len(df):,})")
    return df
