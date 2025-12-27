import requests
import json
import time
import logging
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@dataclass
class PipelineStats:
    """Track pipeline statistics"""
    total: int = 0
    success: int = 0
    failed: int = 0
    retried: int = 0
    start_time: datetime = field(default_factory=datetime.now)
    
    @property
    def duration(self) -> float:
        return (datetime.now() - self.start_time).total_seconds()
    
    @property
    def success_rate(self) -> float:
        return (self.success / self.total * 100) if self.total > 0 else 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "total": self.total,
            "success": self.success,
            "failed": self.failed,
            "retried": self.retried,
            "success_rate": f"{self.success_rate:.1f}%",
            "duration_seconds": f"{self.duration:.2f}"
        }

class ResilientPipeline:
    """A resilient data pipeline with retry logic and rate limiting"""
    
    def __init__(
        self,
        api_key: str,
        calls_per_second: float = 1.0,
        max_retries: int = 3,
        base_delay: float = 1.0
    ):
        self.api_key = api_key
        self.calls_per_second = calls_per_second
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.min_interval = 1.0 / calls_per_second
        self.last_call = 0
        self.stats = PipelineStats()
    
    def _rate_limit(self):
        """Enforce rate limiting"""
        now = time.time()
        elapsed = now - self.last_call
        
        if elapsed < self.min_interval:
            sleep_time = self.min_interval - elapsed
            logger.debug(f"Rate limiting: sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)
        
        self.last_call = time.time()
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=30),
        retry=retry_if_exception_type((
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError
        )),
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )
    def _fetch_single(self, city: str) -> Optional[Dict]:
        """Fetch weather for a single city with retry"""
        self._rate_limit()
        
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": city,
                "appid": self.api_key,
                "units": "metric"
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp_celsius": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "fetched_at": datetime.now().isoformat()
        }
    
    def fetch_city(self, city: str) -> Optional[Dict]:
        """Fetch weather for a city with full error handling"""
        self.stats.total += 1
        
        try:
            result = self._fetch_single(city)
            self.stats.success += 1
            logger.info(f"✓ {city}: {result['temp_celsius']}°C")
            return result
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.warning(f"✗ {city}: not found")
            else:
                logger.error(f"✗ {city}: HTTP {e.response.status_code}")
            self.stats.failed += 1
            return None
            
        except Exception as e:
            logger.error(f"✗ {city}: {e}")
            self.stats.failed += 1
            return None
    
    def fetch_many(self, cities: List[str]) -> List[Dict]:
        """Fetch weather for multiple cities"""
        logger.info(f"Starting pipeline for {len(cities)} cities")
        self.stats = PipelineStats()
        self.stats.total = 0  # Will be updated per city
        
        results = []
        
        for city in cities:
            result = self.fetch_city(city)
            if result:
                results.append(result)
        
        logger.info(f"Pipeline complete: {self.stats.success}/{len(cities)} successful")
        return results
    
    def save_results(
        self,
        results: List[Dict],
        output_path: Path,
        include_stats: bool = True
    ):
        """Save results with optional statistics"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        output = {
            "data": results,
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "record_count": len(results)
            }
        }
        
        if include_stats:
            output["stats"] = self.stats.to_dict()
        
        output_path.write_text(json.dumps(output, indent=2))
        logger.info(f"Saved results to {output_path}")

# Demo
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        print("Set OPENWEATHER_API_KEY in .env")
        exit(1)
    
    # Create pipeline
    pipeline = ResilientPipeline(
        api_key=api_key,
        calls_per_second=1,
        max_retries=3
    )
    
    # Test cities (including some that will fail)
    cities = [
        "Kingston",
        "Bridgetown",
        "Havana",
        "London",
        "Paris",
        "InvalidCity123",  # Will fail
        "Tokyo",
        "New York",
        "AnotherFakeCity",  # Will fail
        "Sydney"
    ]
    
    # Run pipeline
    results = pipeline.fetch_many(cities)
    
    # Save results
    pipeline.save_results(results, Path("output/resilient_weather.json"))
    
    # Print stats
    print("\n=== Pipeline Statistics ===")
    for key, value in pipeline.stats.to_dict().items():
        print(f"  {key}: {value}")