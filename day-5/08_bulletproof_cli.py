import argparse
import logging
import time
import requests
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
import os
from dotenv import load_dotenv

# ============================================================
# SECTION 1: SETUP & CONFIGURATION
# ============================================================

load_dotenv()

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("pipeline")

API_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = os.getenv("OPENWEATHER_API_KEY")


# ============================================================
# SECTION 2: RATE LIMITER
# ============================================================

class RateLimiter:
    """
    Ensures we do not exceed N requests per second.
    """
    def __init__(self, calls_per_second: float):
        self.interval = 1 / calls_per_second
        self.last_call = 0.0

    def wait(self):
        elapsed = time.time() - self.last_call
        if elapsed < self.interval:
            time.sleep(self.interval - elapsed)
        self.last_call = time.time()


# ============================================================
# SECTION 3: CIRCUIT BREAKER
# ============================================================

class CircuitBreaker:
    def __init__(self, max_failures=3, cooldown=15):
        self.max_failures = max_failures
        self.cooldown = cooldown
        self.failures = 0
        self.last_failure_time = None

    def allow(self):
        if self.failures < self.max_failures:
            return True

        elapsed = time.time() - self.last_failure_time
        return elapsed > self.cooldown

    def record_success(self):
        self.failures = 0

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()


# ============================================================
# SECTION 4: RETRY LOGIC (TENACITY)
# ============================================================

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(Exception),
)
def fetch_weather(city: str) -> dict:
    response = requests.get(
        API_URL,
        params={"q": city, "appid": API_KEY, "units": "metric"},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


# ============================================================
# SECTION 5: CORE PIPELINE LOGIC
# ============================================================

def run_pipeline(cities: List[str], output: Path):
    rate_limiter = RateLimiter(calls_per_second=1)
    breaker = CircuitBreaker()
    results = []

    for city in cities:
        logger.info(f"Processing city: {city}")

        if not breaker.allow():
            logger.error("Circuit breaker OPEN — stopping execution")
            break

        try:
            rate_limiter.wait()
            data = fetch_weather(city)
            breaker.record_success()
            results.append(data)
            logger.info(f"Success: {city}")

        except Exception as e:
            breaker.record_failure()
            logger.warning(f"Failure for {city}: {e}")

    # Save results
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json_dump(results))
    logger.info(f"Saved {len(results)} records → {output}")


def json_dump(data):
    import json
    return json.dumps(data, indent=2)


# ============================================================
# SECTION 6: CLI ENTRY POINT
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Bulletproof Weather Pipeline")

    parser.add_argument(
        "--cities",
        required=True,
        help="Comma-separated list of cities"
    )
    parser.add_argument(
        "--output",
        default="output/weather.json",
        help="Output file path"
    )

    args = parser.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENWEATHER_API_KEY not set")

    cities = [c.strip() for c in args.cities.split(",")]

    run_pipeline(cities, Path(args.output))


if __name__ == "__main__":
    main()


