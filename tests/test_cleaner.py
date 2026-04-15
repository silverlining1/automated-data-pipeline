"""Tests for the cleaner module."""

import pandas as pd
import pytest
from pipeline.cleaner import clean_data


SAMPLE_OPEN_METEO = {
    "daily": {
        "time": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "temperature_2m_max": [55.2, 60.1, 48.9],
        "temperature_2m_min": [38.1, 42.3, 35.0],
        "precipitation_sum": [0.0, 0.12, 0.0],
        "windspeed_10m_max": [12.5, 8.3, 15.1],
        "weathercode": [1, 61, 2],
    }
}


def test_clean_open_meteo_dict():
    """clean_data correctly flattens Open-Meteo nested dict."""
    df = clean_data(SAMPLE_OPEN_METEO)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert "date" in df.columns


def test_clean_renames_columns():
    """clean_data renames API field names to readable names."""
    df = clean_data(SAMPLE_OPEN_METEO)
    assert "temp_max_f" in df.columns
    assert "temp_min_f" in df.columns
    assert "precip_in" in df.columns


def test_clean_computes_temp_range():
    """clean_data adds a temp_range_f derived column."""
    df = clean_data(SAMPLE_OPEN_METEO)
    assert "temp_range_f" in df.columns
    assert df["temp_range_f"].iloc[0] == round(55.2 - 38.1, 1)


def test_clean_maps_weather_codes():
    """clean_data maps WMO weather codes to human-readable conditions."""
    df = clean_data(SAMPLE_OPEN_METEO)
    assert "condition" in df.columns
    assert df["condition"].iloc[0] == "Mainly clear"
    assert df["condition"].iloc[1] == "Slight rain"


def test_clean_empty_input():
    """clean_data handles empty input gracefully."""
    result = clean_data([])
    assert isinstance(result, pd.DataFrame)
