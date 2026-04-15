"""Weather KPI computation from cleaned daily forecast DataFrame."""

import logging
import pandas as pd

logger = logging.getLogger(__name__)


def compute_metrics(df: pd.DataFrame) -> dict:
    """Compute weather KPI metrics from the cleaned daily forecast.

    Args:
        df: Cleaned DataFrame with one row per day.

    Returns:
        Dictionary of KPI metrics.
    """
    metrics: dict = {}
    logger.info("Computing weather KPIs")

    metrics["total_days"] = len(df)

    if "date" in df.columns and not df["date"].isna().all():
        metrics["date_from"] = str(df["date"].min().date())
        metrics["date_to"] = str(df["date"].max().date())

    if "temp_max_f" in df.columns:
        metrics["avg_high_f"] = round(df["temp_max_f"].mean(), 1)
        metrics["max_high_f"] = df["temp_max_f"].max()
        metrics["min_high_f"] = df["temp_max_f"].min()

    if "temp_min_f" in df.columns:
        metrics["avg_low_f"] = round(df["temp_min_f"].mean(), 1)

    if "temp_range_f" in df.columns:
        metrics["avg_temp_range_f"] = round(df["temp_range_f"].mean(), 1)

    if "precip_in" in df.columns:
        metrics["total_precip_in"] = round(df["precip_in"].sum(), 2)
        metrics["rainy_days"] = int((df["precip_in"] > 0).sum())

    if "wind_max_mph" in df.columns:
        metrics["avg_wind_mph"] = round(df["wind_max_mph"].mean(), 1)
        metrics["max_wind_mph"] = df["wind_max_mph"].max()

    if "condition" in df.columns:
        metrics["conditions"] = df["condition"].value_counts().to_dict()

    logger.info(f"KPIs computed for {metrics['total_days']} day(s)")
    return metrics
