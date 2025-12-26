#!/bin/bash

# Variables
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="$SCRIPT_DIR/logs/bash_$(date +%Y%m%d_%H%M%S).log"

# Function to log messages
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Create log directory if needed
mkdir -p "$SCRIPT_DIR/logs"

log_message "Starting pipeline runner"

# Check if Python script exists
if [ ! -f "$SCRIPT_DIR/05_organized_pipeline.py" ]; then
    log_message "ERROR: Pipeline script not found"
    exit 1
fi

# Check if .env exists
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    log_message "WARNING: .env file not found"
fi

# Run the pipeline
log_message "Running Python pipeline..."
python "$SCRIPT_DIR/05_organized_pipeline.py"

# Check exit status
if [ $? -eq 0 ]; then
    log_message "Pipeline completed successfully"
else
    log_message "ERROR: Pipeline failed with exit code $?"
    exit 1
fi

# Show output files
log_message "Output files:"
ls -la "$SCRIPT_DIR/output/" | tee -a "$LOG_FILE"

log_message "Done"