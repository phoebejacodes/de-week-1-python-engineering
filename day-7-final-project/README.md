# Weather Data Pipeline

A production-ready data pipeline for fetching and processing weather data.

## Features

- **Multi-source input**: Direct cities, file input, or stdin
- **Multi-format output**: JSON, CSV, Parquet, JSON Lines
- **Resilient**: Retry logic with exponential backoff
- **Rate limited**: Respects API rate limits
- **Comprehensive logging**: File and console logging
- **Statistics**: Tracks success/failure rates and timing

## Installation
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:
```
OPENWEATHER_API_KEY=your_api_key_here
```

## Usage

### Fetch Weather Data
```bash
# From comma-separated cities
python -m src.cli fetch --cities "London,Paris,Tokyo" --output weather.json

# From file
python -m src.cli fetch --file data/cities.txt --output weather.parquet --format parquet

# With verbose logging
python -m src.cli fetch --cities London -v
```

### Convert Between Formats
```bash
python -m src.cli convert weather.json weather.csv --format csv
python -m src.cli convert weather.csv weather.parquet --format parquet
```

### Get File Info
```bash
python -m src.cli info weather.parquet
```

## Project Structure
```
day-7/
├── src/
│   ├── __init__.py     # Package init
│   ├── config.py       # Configuration management
│   ├── api.py          # API client with retry logic
│   ├── pipeline.py     # Pipeline orchestration
│   ├── formats.py      # Data format handlers
│   └── cli.py          # Command-line interface
├── scripts/
│   └── run_pipeline.sh # Automation script
├── data/
│   └── cities.txt      # Sample city list
├── output/             # Generated data files
├── logs/               # Log files
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Architecture
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   CLI       │────▶│  Pipeline   │────▶│  Output     │
│   Input     │     │  Engine     │     │  Formats    │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                    ┌──────┴──────┐
                    │             │
              ┌─────▼─────┐ ┌─────▼─────┐
              │   API     │ │  Logging  │
              │  Client   │ │  Stats    │
              └───────────┘ └───────────┘
```

## Statistics

The pipeline tracks:
- Total requests
- Successful fetches
- Failed fetches
- Success rate
- Execution duration

## Logging

Logs are written to:
- Console (INFO level by default, DEBUG with -v)
- File in `logs/` directory (DEBUG level always)

## License

MIT