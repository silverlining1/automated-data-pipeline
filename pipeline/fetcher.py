"""API data fetcher with retry logic and exponential backoff.

Fetches structured JSON from a REST endpoint, with support for
the Open-Meteo forecast API response format (nested 'daily' key).
"""

import logging
import time
import requests

logger = logging.getLogger(__name__)


def fetch_data(url: str, timeout: int = 15, retries: int = 3, backoff: float = 2.0) -> dict | list | None:
    """Fetch JSON data from a REST API endpoint with retry and exponential backoff.

    Args:
        url: API endpoint URL.
        timeout: Request timeout in seconds.
        retries: Number of retry attempts on failure.
        backoff: Multiplier for exponential backoff between retries.

    Returns:
        Parsed JSON response (dict or list), or None on total failure.
    """
    attempt = 0
    wait = 1.0

    while attempt <= retries:
        try:
            logger.info(f"Fetching data (attempt {attempt + 1}/{retries + 1}): {url[:80]}...")
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            record_hint = len(data) if isinstance(data, list) else "object"
            logger.info(f"Fetch succeeded — response type: {type(data).__name__}, size hint: {record_hint}")
            return data

        except requests.exceptions.Timeout:
            logger.warning(f"Request timed out (attempt {attempt + 1}/{retries + 1})")
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response else "unknown"
            logger.warning(f"HTTP {status} on attempt {attempt + 1}: {e}")
            if e.response and 400 <= e.response.status_code < 500:
                logger.error("Client error — not retrying.")
                return None
        except requests.exceptions.ConnectionError:
            logger.warning(f"Connection error on attempt {attempt + 1}")
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request error on attempt {attempt + 1}: {e}")
        except ValueError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return None

        attempt += 1
        if attempt <= retries:
            logger.info(f"Retrying in {wait:.1f}s...")
            time.sleep(wait)
            wait *= backoff

    logger.error(f"All {retries + 1} fetch attempts failed.")
    return None
