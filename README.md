# Data Engineering Fundamentals: Python & Bash

Building production-ready data pipelines from scratch. This repository documents my journey into data engineering, demonstrating core skills required for the role.

## 🎯 What This Demonstrates

- **API Integration**: Fetching data from REST APIs with authentication
- **Error Handling**: Robust try/except patterns, retries, graceful failures
- **Logging**: Professional logging replacing print statements
- **File I/O**: Reading/writing JSON, CSV, Parquet formats
- **CLI Tools**: Command-line interfaces with argparse
- **Project Structure**: Organized, maintainable code architecture
- **Bash Scripting**: Automation and environment management

## 📁 Project Structure
```
.
├── day-1-api-basics/
│   ├── 01_first_api_call.py
│   ├── 02_json_parsing.py
│   ├── 03_nested_json.py
│   ├── 04_query_parameters.py
│   ├── 05_write_to_file.py
│   └── 06_complete_pipeline.py
├── day-2-error-handling/
│   ├── 01_things_that_break.py
│   ├── 02_try_except_basics.py
│   ├── 03_safe_api_calls.py
│   └── 07_robust_pipeline.py
├── day-3-logging/
│   ├── 01_logging_basics.py
│   ├── 03_pipeline_with_logging.py
│   └── 05_organized_pipeline.py
├── day-4-cli-tools/
│   └── weather_cli.py
├── day-5-resilience/
│   └── resilient_pipeline.py
├── day-6-data-formats/
│   └── format_converter.py
├── day-7-final-project/
│   ├── src/
│   ├── scripts/
│   ├── data/
│   └── output/
├── requirements.txt
└── README.md
```

## 🚀 Featured Project: Weather Data Pipeline

A complete ETL pipeline that:

1. Reads city list from input file
2. Fetches weather data from OpenWeatherMap API
3. Handles failures gracefully with retry logic
4. Transforms and validates data
5. Outputs to multiple formats (JSON, CSV, Parquet)
6. Logs all operations with timestamps

### Architecture
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Input      │────▶│  API        │────▶│  Transform  │────▶│  Output     │
│  cities.txt │     │  Fetch      │     │  & Validate │     │  JSON/CSV   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  Logging    │
                    │  & Errors   │
                    └─────────────┘
```

### Usage
```bash
# Clone repository
git clone https://github.com/phoebejacodes/de-week-1-python-engineering.git
cd de-week-1-python-engineering

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your API key

# Run the pipeline
python -m day-7-final-project.src.pipeline

# Or use CLI
python day-7-final-project/weather_cli.py --cities London,Tokyo,Paris --output data/weather.json
```

### Sample Output
```json
[
  {
    "city": "London",
    "country": "GB",
    "temp_celsius": 12.5,
    "humidity": 76,
    "description": "scattered clouds",
    "fetched_at": "2024-01-15T10:30:00"
  }
]
```

## 🛠️ Technologies Used

| Category | Tools |
|----------|-------|
| Language | Python 3.10+ |
| HTTP | requests |
| Data Formats | json, csv, pyarrow (Parquet) |
| Configuration | python-dotenv |
| CLI | argparse |
| Scripting | Bash |

## 📚 Key Learnings

### Error Handling Pattern
```python
def fetch_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP Error: {e.response.status_code}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None
```

### Logging Configuration
```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)
```

### Retry Logic
```python
def fetch_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        result = fetch_data(url)
        if result:
            return result
        time.sleep(2 ** attempt)  # Exponential backoff
    return None
```

## 🔜 Next Steps

This repository is Week 1 of my data engineering journey. Upcoming:

- **Week 2-3**: AWS (S3, IAM, Glue, Athena)
- **Week 4-5**: Snowflake & Data Warehousing
- **Week 6-7**: dbt (Data Build Tool)
- **Week 8-9**: Apache Airflow
- **Week 10+**: End-to-end portfolio project
