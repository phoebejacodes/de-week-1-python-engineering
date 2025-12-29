"""API client for weather data"""

import requests
import time
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from dataclasses import dataclass, field
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)

from .config import PipelineConfig

logger = logging.getLogger(__name__)

@dataclass
class WeatherData:
    """Weather data for a city"""
    city: str
    country: str
    temp_celsius: float
    humidity: int
    description: str
    wind_speed: float
    fetched_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "city": self.city,
            "country": self.country,
            "temp_celsius": self.temp_celsius,
            "humidity": self.humidity,
            "description": self.description,
            "wind_speed": self.wind_speed,
            "fetched_at": self.fetched_at
        }

class RateLimiter:
    """Simple rate limiter"""
    
    def __init__(self, calls_per_second: float):
        self.min_interval = 1.0 / calls_per_second
        self.last_call = 0.0
    
    def wait(self):
        """Wait if necessary to respect rate limit"""
        now = time.time()
        elapsed = now - self.last_call
        
        if elapsed < self.min_interval:
            sleep_time = self.min_interval - elapsed
            logger.debug(f"Rate limiting: waiting {sleep_time:.2f}s")
            time.sleep(sleep_time)
        
        self.last_call = time.time()

class WeatherAPIClient:
    """Client for OpenWeatherMap API"""
    
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.rate_limiter = RateLimiter(config.calls_per_second)
        self._setup_retry()
    
    def _setup_retry(self):
        """Configure retry decorator"""
        self._fetch_with_retry = retry(
            stop=stop_after_attempt(self.config.max_retries),
            wait=wait_exponential(
                multiplier=self.config.base_delay,
                min=self.config.base_delay,
                max=self.config.max_delay
            ),
            retry=retry_if_exception_type((
                requests.exceptions.Timeout,
                requests.exceptions.ConnectionError
            )),
            before_sleep=before_sleep_log(logger, logging.WARNING)
        )(self._fetch_raw)
    
    def _fetch_raw(self, city: str) -> Dict[str, Any]:
        """Raw fetch without retry (retry is applied via decorator)"""
        self.rate_limiter.wait()
        
        response = requests.get(
            self.config.api_base_url,
            params={
                "q": city,
                "appid": self.config.api_key,
                "units": "metric"
            },
            timeout=self.config.api_timeout
        )
        response.raise_for_status()
        return response.json()
    
    def fetch(self, city: str) -> Optional[WeatherData]:
        """Fetch weather data for a city"""
        logger.debug(f"Fetching weather for {city}")
        
        try:
            data = self._fetch_with_retry(city)
            
            weather = WeatherData(
                city=data["name"],
                country=data["sys"]["country"],
                temp_celsius=data["main"]["temp"],
                humidity=data["main"]["humidity"],
                description=data["weather"][0]["description"],
                wind_speed=data["wind"]["speed"]
            )
            
            logger.info(f"✓ {city}: {weather.temp_celsius}°C, {weather.description}")
            return weather
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.warning(f"✗ {city}: not found")
            else:
                logger.error(f"✗ {city}: HTTP {e.response.status_code}")
            return None
            
        except Exception as e:
            logger.error(f"✗ {city}: {e}")
            return None