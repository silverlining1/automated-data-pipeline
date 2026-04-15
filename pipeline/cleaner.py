"""Data cleaning and normalization for Open-Meteo API responses.

The Open-Meteo API returns a nested dict with a 'daily' key containing
parallel arrays. This module flattens that into a row-per-day DataFrame.
"""

import logging
import pandas as pd

logger = logging.getLogger(__name__)

WMO_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def clean_data(raw_data: dict | list) -> pd.DataFrame:
    """Convert Open-Meteo API response into a clean, analysis-ready DataFrame.

    Args:
        raw_data: JSON response from Open-Meteo (dict with 'daily' key).

    Returns:
        Cleaned pandas DataFrame with one row per day.

    Raises:
        ValueError: If the response format is unexpected.
    """
    if isinstance(raw_data, list):
        logger.info("Received list payload — converting directly to DataFrame")
        df = pd.DataFrame(raw_data)
    elif isinstance(raw_data, dict) and "daily" in raw_data:
        logger.info("Received Open-Meteo dict payload — flattening 'daily' arrays")
        daily = raw_data["daily"]
        df = pd.DataFrame(daily)
    elif isinstance(raw_data, dict):
        logger.info("Received generic dict payload — wrapping as single row")
        df = pd.DataFrame([raw_data])
    else:
        logger.error(f"Unexpected raw_data type: {type(raw_data)}")
        return pd.DataFrame()

    initial_rows = len(df)
    logger.info(f"Raw shape: {initial_rows} rows × {len(df.columns)} columns")

    # Rename columns for readability
    rename_map = {
        "time": "date",
        "temperature_2m_max": "temp_max_f",
        "temperature_2m_min": "temp_min_f",
        "precipitation_sum": "precip_in",
        "windspeed_10m_max": "wind_max_mph",
        "weathercode": "weather_code",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    # Convert date
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Coerce numeric columns
    for col in ["temp_max_f", "temp_min_f", "precip_in", "wind_max_mph", "weather_code"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Compute temp range
    if "temp_max_f" in df.columns and "temp_min_f" in df.columns:
        df["temp_range_f"] = (df["temp_max_f"] - df["temp_min_f"]).round(1)

    # Map WMO weather codes to readable descriptions
    if "weather_code" in df.columns:
        df["condition"] = df["weather_code"].map(WMO_CODES).fillna("Unknown")

    # Drop fully null rows
    df = df.dropna(how="all").reset_index(drop=True)

    logger.info(f"Cleaned shape: {len(df)} rows × {len(df.columns)} columns")
    return df
