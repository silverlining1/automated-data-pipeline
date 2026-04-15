"""Central configuration loaded from environment variables."""

import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "https://jsonplaceholder.typicode.com/posts")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))
RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", "3"))
RETRY_BACKOFF = float(os.getenv("RETRY_BACKOFF", "2.0"))
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "outputs")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
