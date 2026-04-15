"""Tests for the fetcher module using mocked HTTP requests."""

import pytest
from unittest.mock import patch, MagicMock
from pipeline.fetcher import fetch_data


@patch("pipeline.fetcher.requests.get")
def test_fetch_success(mock_get):
    """fetch_data returns parsed JSON on a 200 response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"daily": {"time": ["2024-01-01"]}}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fetch_data("https://example.com/api", retries=0)
    assert result == {"daily": {"time": ["2024-01-01"]}}


@patch("pipeline.fetcher.requests.get")
def test_fetch_404_no_retry(mock_get):
    """fetch_data returns None on 404 without retrying."""
    import requests

    mock_response = MagicMock()
    mock_response.status_code = 404
    http_error = requests.exceptions.HTTPError(response=mock_response)
    mock_response.raise_for_status.side_effect = http_error
    mock_get.return_value = mock_response

    result = fetch_data("https://example.com/api", retries=2)
    assert result is None
    assert mock_get.call_count == 1  # Should not retry on 404


@patch("pipeline.fetcher.requests.get")
@patch("pipeline.fetcher.time.sleep", return_value=None)
def test_fetch_retries_on_timeout(mock_sleep, mock_get):
    """fetch_data retries on timeout up to the specified limit."""
    import requests

    mock_get.side_effect = requests.exceptions.Timeout()
    result = fetch_data("https://example.com/api", retries=2)
    assert result is None
    assert mock_get.call_count == 3  # initial + 2 retries
