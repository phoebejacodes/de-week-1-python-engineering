import argparse
import requests
import json
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

def setup_logging(verbose):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)

def fetch_weather(city, api_key, logger):
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
        logger.error(f"Failed: {city} - {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Fetch weather from city list file")
    
    # Accept either direct cities OR a file
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--cities", "-c", help="Comma-separated cities")
    group.add_argument("--file", "-f", type=Path, help="File with cities (one per line)")
    
    parser.add_argument("--output", "-o", default="output/weather.json")
    parser.add_argument("--verbose", "-v", action="store_true")
    
    args = parser.parse_args()
    logger = setup_logging(args.verbose)
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        logger.error("API key not set")
        return 1
    
    # Get cities from either source
    if args.cities:
        cities = [c.strip() for c in args.cities.split(",")]
    else:
        if not args.file.exists():
            logger.error(f"File not found: {args.file}")
            return 1
        cities = args.file.read_text().strip().split("\n")
    
    logger.info(f"Processing {len(cities)} cities")
    
    # Fetch
    results = []
    for city in cities:
        weather = fetch_weather(city, api_key, logger)
        if weather:
            results.append(weather)
    
    # Save
    if results:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(results, indent=2))
        logger.info(f"Saved to {output_path}")
    
    return 0

if __name__ == "__main__":
    exit(main())