"""API data fetcher with retry logic and exponential backoff."""

import logging
import time
import requests

logger = logging.getLogger(__name__)


def fetch_data(url: str, timeout: int = 10, retries: int = 3, backoff: float = 2.0) -> list | None:
    """Fetch JSON data from a REST API endpoint with retry and backoff.

    Args:
        url: API endpoint URL.
        timeout: Request timeout in seconds.
        retries: Number of retry attempts on failure.
        backoff: Multiplier for exponential backoff between retries.

    Returns:
        Parsed JSON data (list or dict), or None on total failure.
    """
    attempt = 0
    wait = 1.0

    while attempt <= retries:
        try:
            logger.info(f"Fetching data (attempt {attempt + 1}/{retries + 1}): {url}")
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Successfully fetched {len(data) if isinstance(data, list) else 1} record(s)")
            return data

        except requests.exceptions.Timeout:
            logger.warning(f"Request timed out (attempt {attempt + 1})")
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response else "unknown"
            logger.warning(f"HTTP {status} error on attempt {attempt + 1}: {e}")
            # Don't retry on client errors (4xx)
            if e.response and 400 <= e.response.status_code < 500:
                logger.error("Client error — not retrying.")
                return None
        except requests.exceptions.ConnectionError:
            logger.warning(f"Connection error on attempt {attempt + 1}")
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request error on attempt {attempt + 1}: {e}")

        attempt += 1
        if attempt <= retries:
            logger.info(f"Retrying in {wait:.1f} seconds...")
            time.sleep(wait)
            wait *= backoff

    logger.error(f"All {retries + 1} attempts failed for {url}")
    return None
