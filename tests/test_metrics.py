"""Tests for the KPI metrics module."""

import pandas as pd
import pytest
from pipeline.metrics import compute_metrics


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "date": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
        "temp_max_f": [55.0, 62.0, 48.0],
        "temp_min_f": [38.0, 44.0, 35.0],
        "temp_range_f": [17.0, 18.0, 13.0],
        "precip_in": [0.0, 0.15, 0.0],
        "wind_max_mph": [10.0, 8.0, 14.0],
        "condition": ["Clear sky", "Slight rain", "Partly cloudy"],
    })


def test_total_days(sample_df):
    m = compute_metrics(sample_df)
    assert m["total_days"] == 3


def test_avg_high(sample_df):
    m = compute_metrics(sample_df)
    assert m["avg_high_f"] == round((55 + 62 + 48) / 3, 1)


def test_total_precip(sample_df):
    m = compute_metrics(sample_df)
    assert m["total_precip_in"] == 0.15


def test_rainy_days(sample_df):
    m = compute_metrics(sample_df)
    assert m["rainy_days"] == 1


def test_conditions_present(sample_df):
    m = compute_metrics(sample_df)
    assert "conditions" in m
    assert "Slight rain" in m["conditions"]
