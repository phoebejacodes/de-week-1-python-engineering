import argparse
import requests
import json
import csv
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

def setup_logging(verbose):
    """Configure logging based on verbosity"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)

def fetch_weather(city, api_key, logger):
    """Fetch weather for a single city"""
    logger.debug(f"Fetching weather for {city}")
    
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
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "fetched_at": datetime.now().isoformat()
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch {city}: {e}")
        return None

def save_results(results, output_path, format_type, logger):
    """Save results in specified format"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if format_type == "json":
        output_path.write_text(json.dumps(results, indent=2))
    elif format_type == "csv":
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
    
    logger.info(f"Saved {len(results)} records to {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Fetch weather data for cities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python 05_weather_cli.py London,Paris,Tokyo
  python 05_weather_cli.py London --output weather.json
  python 05_weather_cli.py London,Paris --format csv -v
        """
    )
    
    parser.add_argument(
        "cities",
        help="Comma-separated list of cities"
    )
    parser.add_argument(
        "--output", "-o",
        default="output/weather.json",
        help="Output file path (default: output/weather.json)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["json", "csv"],
        default="json",
        help="Output format (default: json)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Setup
    logger = setup_logging(args.verbose)
    logger.info("Weather CLI started")
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        logger.error("OPENWEATHER_API_KEY not set in environment")
        return 1
    
    # Parse cities
    cities = [c.strip() for c in args.cities.split(",")]
    logger.info(f"Fetching weather for {len(cities)} cities")
    
    # Fetch data
    results = []
    for city in cities:
        weather = fetch_weather(city, api_key, logger)
        if weather:
            results.append(weather)
            logger.debug(f"  {city}: {weather['temp_celsius']}°C")
    
    # Save results
    if results:
        save_results(results, args.output, args.format, logger)
    else:
        logger.warning("No data to save")
        return 1
    
    logger.info("Done")
    return 0

if __name__ == "__main__":
    exit(main())