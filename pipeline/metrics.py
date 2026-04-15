"""KPI computation from cleaned DataFrame."""

import logging
import pandas as pd

logger = logging.getLogger(__name__)


def compute_metrics(df: pd.DataFrame) -> dict:
    """Compute KPI metrics from the cleaned dataset.

    Adapts to whatever columns are present in the data.

    Args:
        df: Cleaned DataFrame.

    Returns:
        Dictionary of KPI metrics.
    """
    metrics = {}
    logger.info("Computing KPIs")

    metrics["total_records"] = len(df)
    metrics["total_columns"] = len(df.columns)
    metrics["columns"] = df.columns.tolist()

    # Count of records by any groupable column (first string column with < 50 unique values)
    for col in df.select_dtypes(include="object").columns:
        if df[col].nunique() < 50:
            metrics["top_group_column"] = col
            metrics["records_by_group"] = df[col].value_counts().head(10).to_dict()
            break

    # Numeric column summaries
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    metrics["numeric_summaries"] = {}
    for col in numeric_cols[:5]:  # Cap at 5 to keep report readable
        metrics["numeric_summaries"][col] = {
            "mean": round(df[col].mean(), 2),
            "min": df[col].min(),
            "max": df[col].max(),
        }

    logger.info(f"KPIs computed for {metrics['total_records']:,} records")
    return metrics
