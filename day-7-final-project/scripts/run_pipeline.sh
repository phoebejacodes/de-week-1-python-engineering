#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "=== Weather Pipeline Runner ==="
echo ""

# Check for .env
if [ ! -f "../.env" ]; then
    echo "Warning: .env file not found in project root"
fi

# Run fetch
echo "Running fetch command..."
python -m src.cli fetch --file data/cities.txt --output output/weather.json --verbose

echo ""
echo "Converting to other formats..."
python -m src.cli convert output/weather.json output/weather.csv --format csv
python -m src.cli convert output/weather.json output/weather.parquet --format parquet

echo ""
echo "File info:"
python -m src.cli info output/weather.parquet

echo ""
echo "=== Complete ==="