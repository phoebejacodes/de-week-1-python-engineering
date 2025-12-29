# Day 7: Integration Project

**Project:** A complete weather data pipeline CLI tool.

**Features:**
1. Fetch weather data from API
2. Support multiple input sources (direct cities, file, stdin)
3. Output to multiple formats (JSON, CSV, Parquet)
4. Retry logic with exponential backoff
5. Rate limiting
6. Comprehensive logging
7. Statistics and reporting
8. Subcommands (fetch, convert, info)

**Project structure:**
```
day-7/
├── src/
│   ├── __init__.py        # Makes this a package
│   ├── config.py          # Settings, constants, environment variables
│   ├── api.py             # Fetching data (network logic)
│   ├── pipeline.py        # Orchestration / business logic
│   ├── formats.py         # CSV / JSON / Parquet handling
│   └── cli.py             # Command-line interface (argparse)
│
├── scripts/
│   └── run_pipeline.sh    # Shell wrapper (optional)
│
├── data/
│   └── cities.txt         # Input data
│
├── output/                # Generated files
├── logs/                  # Execution logs
├── requirements.txt
└── README.md
```

## Mental Model

USER
 │
 ▼
CLI (argparse)
 │
 ▼
Validation & Parsing
 │
 ▼
Pipeline Controller
 │
 ├──> Rate Limiter
 ├──> Retry Logic
 ├──> API Client
 │        ↓
 │     Raw Data
 │
 ├──> Transformer (formatting)
 │
 └──> Output Writer (CSV / JSON / Parquet)
         ↓
       Files + Logs

