import requests
import logging
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
    after_log
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Basic retry decorator
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(requests.exceptions.RequestException),
    before_sleep=before_sleep_log(logger, logging.WARNING)
)
def fetch_with_tenacity(url, timeout=10):
    """Fetch URL with automatic retry using tenacity"""
    logger.info(f"Fetching: {url}")
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.json()

# More sophisticated retry with custom conditions
def is_retryable_error(exception):
    """Determine if we should retry based on exception"""
    if isinstance(exception, requests.exceptions.HTTPError):
        # Retry on 5xx errors, not on 4xx
        return 500 <= exception.response.status_code < 600
    return isinstance(exception, (
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError
    ))

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry=retry_if_exception_type((
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError
    )),
    before_sleep=before_sleep_log(logger, logging.WARNING)
)
def fetch_robust(url, timeout=10):
    """More robust fetch with selective retry"""
    logger.info(f"Fetching: {url}")
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.json()

# Test
print("=== Test 1: Working URL ===")
try:
    data = fetch_with_tenacity("https://httpbin.org/json")
    print(f"Success: got {list(data.keys())}")
except Exception as e:
    print(f"Failed: {e}")

print("\n=== Test 2: Failing URL (will retry) ===")
try:
    data = fetch_with_tenacity("https://httpbin.org/status/500")
    print(f"Success: {data}")
except Exception as e:
    print(f"Failed after retries: {type(e).__name__}")

print("=== Test 3: Working URL Robust ===")
try:
    data = fetch_robust("https://httpbin.org/json")
    print(f"Success: got {list(data.keys())}")
except Exception as e:
    print(f"Failed: {e}")

print("\n=== Test 4: Failing URL (will retry) Robust ===")
try:
    data = fetch_robust("https://httpbin.org/status/500")
    print(f"Success: {data}")
except Exception as e:
    print(f"Failed after retries: {type(e).__name__}")