#!/bin/bash

# =====================
# Weather Pipeline Runner
# =====================

# Configuration
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PYTHON_SCRIPT="$PROJECT_DIR/day-4/06_file_input_cli.py"
DEFAULT_CITIES_FILE="$PROJECT_DIR/day-4/cities.txt"
OUTPUT_DIR="$PROJECT_DIR/day-4/output"
LOG_FILE="$OUTPUT_DIR/run_$(date +%Y%m%d_%H%M%S).log"

# Functions
log() {
    local message=$1
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $message" | tee -a "$LOG_FILE"
}

check_requirements() {
    log "Checking requirements..."
    
    if [ ! -f "$PYTHON_SCRIPT" ]; then
        log "ERROR: Python script not found: $PYTHON_SCRIPT"
        return 1
    fi
    
    if [ -z "$OPENWEATHER_API_KEY" ]; then
    log "Loading environment variables from .env"
    
        if [ -f "$PROJECT_DIR/.env" ]; then
        set -a
        source "$PROJECT_DIR/.env"
        set +a
        fi
    fi

    
    if [ -z "$OPENWEATHER_API_KEY" ]; then
        log "ERROR: OPENWEATHER_API_KEY not available"
        return 1
    fi
    
    log "Requirements OK"
    return 0
}

run_pipeline() {
    local cities_file=$1
    local output_file=$2
    
    log "Running pipeline..."
    log "  Cities file: $cities_file"
    log "  Output file: $output_file"
    
    python "$PYTHON_SCRIPT" --file "$cities_file" --output "$output_file" --verbose
    
    if [ $? -eq 0 ]; then
        log "Pipeline completed successfully"
        return 0
    else
        log "ERROR: Pipeline failed"
        return 1
    fi
}

show_usage() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -f, --file FILE    Cities file (default: cities.txt)"
    echo "  -o, --output FILE  Output file (default: auto-generated)"
    echo "  -h, --help         Show this help"
    echo ""
    echo "Example:"
    echo "  $0"
    echo "  $0 --file my_cities.txt"
    echo "  $0 --file cities.txt --output weather.json"
}

# ===================
# Main
# ===================

# Default values
CITIES_FILE="$DEFAULT_CITIES_FILE"
OUTPUT_FILE="$OUTPUT_DIR/weather_$(date +%Y%m%d_%H%M%S).json"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--file)
            CITIES_FILE="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Run
log "========================================"
log "Weather Pipeline Started"
log "========================================"

if ! check_requirements; then
    log "Requirements check failed"
    exit 1
fi

if ! run_pipeline "$CITIES_FILE" "$OUTPUT_FILE"; then
    log "Pipeline failed"
    exit 1
fi

log "========================================"
log "Pipeline Finished"
log "========================================"
log "Output: $OUTPUT_FILE"

# Show output
echo ""
echo "=== Results ==="
cat "$OUTPUT_FILE"