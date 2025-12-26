from pathlib import Path
from dotenv import load_dotenv
import os
import requests
import json
import csv
import logging
from datetime import datetime

# Setup directories
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

# Create directories
for dir_path in [DATA_DIR, OUTPUT_DIR, LOG_DIR]:
    dir_path.mkdir(exist_ok=True)

# Configure logging
log_file = LOG_DIR / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def load_cities():
    """Load cities from input file"""
    cities_file = DATA_DIR / "cities.txt"
    
    if not cities_file.exists():
        logger.warning(f"Cities file not found, creating default: {cities_file}")
        cities_file.write_text("Kingston\nLondon\nTokyo\nNew York\n")
    
    cities = cities_file.read_text().strip().split("\n")
    logger.info(f"Loaded {len(cities)} cities from {cities_file}")
    return cities

def fetch_weather(city):
    """Fetch weather for a single city"""
    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": API_KEY, "units": "metric"},
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
    except Exception as e:
        logger.error(f"Failed to fetch {city}: {e}")
        return None

def save_results(results):
    """Save results to output files"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # JSON
    json_file = OUTPUT_DIR / f"weather_{timestamp}.json"
    json_file.write_text(json.dumps(results, indent=2))
    logger.info(f"Wrote JSON: {json_file}")
    
    # CSV
    csv_file = OUTPUT_DIR / f"weather_{timestamp}.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    logger.info(f"Wrote CSV: {csv_file}")

def main():
    logger.info("Pipeline started")
    logger.info(f"Base directory: {BASE_DIR}")
    logger.info(f"Log file: {log_file}")
    
    if not API_KEY:
        logger.critical("API key not set")
        return
    
    cities = load_cities()
    results = []
    
    for city in cities:
        weather = fetch_weather(city)
        if weather:
            results.append(weather)
    
    if results:
        save_results(results)
    
    logger.info(f"Pipeline completed: {len(results)} records")

if __name__ == "__main__":
    main()
