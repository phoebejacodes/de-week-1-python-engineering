import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def fetch_weather(city, api_key):
    """Fetch weather for a city"""
    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": api_key, "units": "metric"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp_celsius": data["main"]["temp"],
            "fetched_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to fetch {city}: {e}")
        return None