import json
import csv
import logging
from datetime import datetime
from pathlib import Path

from . import config
from .api import fetch_weather

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    # Create directories
    for d in [config.DATA_DIR, config.OUTPUT_DIR, config.LOG_DIR]:
        d.mkdir(exist_ok=True)
    
    # Load cities
    cities_file = config.DATA_DIR / "cities.txt"
    cities = cities_file.read_text().strip().split("\n")
    
    # Fetch data
    results = []
    for city in cities:
        data = fetch_weather(city, config.OPENWEATHER_API_KEY)
        if data:
            results.append(data)
    
    # Save
    if results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = config.OUTPUT_DIR / f"weather_{timestamp}.json"
        output_file.write_text(json.dumps(results, indent=2))
        logger.info(f"Saved {len(results)} records to {output_file}")

if __name__ == "__main__":
    main()