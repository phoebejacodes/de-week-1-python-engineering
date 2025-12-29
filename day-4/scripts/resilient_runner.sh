#!/bin/bash

set -e  # Exit on error
set -u  # Exit on undefined variable
set -o pipefail  # Exit on pipe failure

# Configuration
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$PROJECT_DIR/day-5/logs"
MAX_RETRIES=3
RETRY_DELAY=5

# Create log directory
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/runner_$(date +%Y%m%d_%H%M%S).log"

# Logging function
log() {
    local level=$1
    local message=$2
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message" | tee -a "$LOG_FILE"
}

# Retry function
retry_command() {
    local cmd=$1
    local retries=0
    
    while [ $retries -lt $MAX_RETRIES ]; do
        log "INFO" "Attempt $((retries + 1))/$MAX_RETRIES: $cmd"
        
        if eval "$cmd"; then
            log "INFO" "Command succeeded"
            return 0
        else
            retries=$((retries + 1))
            if [ $retries -lt $MAX_RETRIES ]; then
                log "WARNING" "Command failed, retrying in ${RETRY_DELAY}s..."
                sleep $RETRY_DELAY
            fi
        fi
    done
    
    log "ERROR" "Command failed after $MAX_RETRIES attempts"
    return 1
}

# Cleanup function (runs on exit)
cleanup() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        log "ERROR" "Script failed with exit code $exit_code"
    else
        log "INFO" "Script completed successfully"
    fi
}

trap cleanup EXIT

# Main
log "INFO" "========================================"
log "INFO" "Resilient Runner Started"
log "INFO" "========================================"

# Example: Run Python script with retry
log "INFO" "Running resilient pipeline..."

if retry_command "python $PROJECT_DIR/day-5/06_resilient_pipeline.py"; then
    log "INFO" "Pipeline completed successfully"
else
    log "ERROR" "Pipeline failed"
    exit 1
fi

log "INFO" "========================================"
log "INFO" "Runner Finished"
log "INFO" "========================================"