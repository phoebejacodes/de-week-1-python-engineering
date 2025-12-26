from dotenv import load_dotenv
import os
import requests
import json
import csv
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city):
    """Fetch weather for a single city"""
    logger.debug(f"Fetching weather for {city}")
    
    try:
        response = requests.get(
            BASE_URL,
            params={"q": city, "appid": API_KEY, "units": "metric"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        result = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp_celsius": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "fetched_at": datetime.now().isoformat()
        }
        
        logger.info(f"Successfully fetched {city}: {result['temp_celsius']}°C")
        return result
        
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP Error for {city}: {e.response.status_code}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for {city}: {e}")
        return None
    except KeyError as e:
        logger.error(f"Missing data for {city}: {e}")
        return None

def main():
    logger.info("=" * 50)
    logger.info("Weather Pipeline Started")
    logger.info("=" * 50)
    
    if not API_KEY:
        logger.critical("OPENWEATHER_API_KEY not set - exiting")
        return

    cities = ["London", "Tokyo", "New York", "Paris", "Kingston", "InvalidCity123", "Berlin"]

    results = []
    failed = []
    
    logger.info(f"Processing {len(cities)} cities")
    
    for city in cities:
        weather = fetch_weather(city)
        if weather:
            results.append(weather)
        else:
            failed.append(city)
    
    logger.info(f"Completed: {len(results)} success, {len(failed)} failed")
    
    if failed:
        logger.warning(f"Failed cities: {failed}")
    
    if results:
        with open("weather_data.json", "w") as f:
            json.dump(results, f, indent=2)
        logger.info(f"Wrote {len(results)} records to weather_data.json")
        
        with open("weather_data.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        logger.info(f"Wrote {len(results)} records to weather_data.csv")
    
    logger.info("Pipeline completed")

if __name__ == "__main__":
    main()