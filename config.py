"""Central configuration loaded from environment variables.

Default: fetches 7-day historical weather data for Atlanta, GA
from the Open-Meteo free API (no key required).
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Open-Meteo historical weather endpoint (free, no API key required)
# Change LAT/LON for your city
LATITUDE = os.getenv("LATITUDE", "33.749")
LONGITUDE = os.getenv("LONGITUDE", "-84.388")
CITY_NAME = os.getenv("CITY_NAME", "Atlanta, GA")
FORECAST_DAYS = int(os.getenv("FORECAST_DAYS", "7"))

API_URL = os.getenv(
    "API_URL",
    (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LATITUDE}&longitude={LONGITUDE}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,"
        f"windspeed_10m_max,weathercode"
        f"&temperature_unit=fahrenheit"
        f"&windspeed_unit=mph"
        f"&precipitation_unit=inch"
        f"&forecast_days={FORECAST_DAYS}"
        f"&timezone=America/New_York"
    ),
)

API_TIMEOUT = int(os.getenv("API_TIMEOUT", "15"))
RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", "3"))
RETRY_BACKOFF = float(os.getenv("RETRY_BACKOFF", "2.0"))
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "outputs")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
