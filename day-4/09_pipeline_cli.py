import argparse
import requests
import json
import logging
from pathlib import Path
from datetime import datetime
import os
from dotenv import load_dotenv


# -----------------------------
# Setup
# -----------------------------
load_dotenv()

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

API_KEY = os.getenv("OPENWEATHER_API_KEY")


# -----------------------------
# Logging
# -----------------------------
def setup_logging(verbose: bool):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)


# -----------------------------
# Fetch Weather
# -----------------------------
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
            "description": data["weather"][0]["description"],
            "fetched_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to fetch {city}: {e}")
        return None


# -----------------------------
# SUBCOMMANDS
# -----------------------------
def cmd_fetch(args):
    logger = setup_logging(args.verbose)

    if not API_KEY:
        logger.error("OPENWEATHER_API_KEY not set")
        return

    if args.cities:
        cities = [c.strip() for c in args.cities.split(",")]
    else:
        cities = Path(args.file).read_text().splitlines()

    results = []
    for city in cities:
        data = fetch_weather(city, API_KEY, logger)
        if data:
            results.append(data)

    if not results:
        logger.warning("No results fetched")
        return

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.format == "json":
        output_path.write_text(json.dumps(results, indent=2))
    else:
        import csv
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

    logger.info(f"Saved {len(results)} records to {output_path}")


def cmd_convert(args):
    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print("Input file not found")
        return

    with open(input_path) as f:
        data = json.load(f)

    if args.format == "csv":
        import csv
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    else:
        output_path.write_text(json.dumps(data, indent=2))

    print(f"Converted file written to {output_path}")


def cmd_info(args):
    path = Path(args.file)
    if not path.exists():
        print("File not found")
        return

    if path.suffix == ".json":
        data = json.loads(path.read_text())
        print(f"Records: {len(data)}")
        print("Fields:", list(data[0].keys()))
    else:
        print("Unsupported file type")



# -----------------------------
# CLI Definition
# -----------------------------
def main():
    parser = argparse.ArgumentParser(description="Weather Data CLI")
    subparsers = parser.add_subparsers(dest="command")

    # FETCH
    fetch = subparsers.add_parser("fetch", help="Fetch weather data")
    fetch.add_argument("--cities", help="Comma-separated cities")
    fetch.add_argument("--file", help="File with city names")
    fetch.add_argument("--output", default="output/weather.json")
    fetch.add_argument("--format", choices=["json", "csv"], default="json")
    fetch.add_argument("--verbose", "-v", action="store_true")
    fetch.set_defaults(func=cmd_fetch)

    # CONVERT
    convert = subparsers.add_parser("convert", help="Convert data format")
    convert.add_argument("input", help="Input file")
    convert.add_argument("--output", required=True)
    convert.add_argument("--format", choices=["json", "csv"], required=True)
    convert.set_defaults(func=cmd_convert)

    # INFO
    info = subparsers.add_parser("info", help="Inspect data file")
    info.add_argument("file")
    info.set_defaults(func=cmd_info)

    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return

    args.func(args)

if __name__ == "__main__":
    main()

