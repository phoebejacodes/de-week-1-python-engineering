import argparse
import os
from pathlib import Path

def get_config():
    """Build configuration from multiple sources"""
    
    parser = argparse.ArgumentParser(description="Configurable CLI tool")
    
    # Arguments with environment variable fallbacks
    parser.add_argument(
        "--api-key",
        default=os.environ.get("OPENWEATHER_API_KEY"),
        help="API key (or set OPENWEATHER_API_KEY env var)"
    )
    parser.add_argument(
        "--output-dir",
        default=os.environ.get("OUTPUT_DIR", "output"),
        help="Output directory (or set OUTPUT_DIR env var)"
    )
    parser.add_argument(
        "--log-level",
        default=os.environ.get("LOG_LEVEL", "INFO"),
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (or set LOG_LEVEL env var)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Override log level to DEBUG"
    )
    
    args = parser.parse_args()
    
    # Verbose flag overrides log level
    if args.verbose:
        args.log_level = "DEBUG"
    
    return args

def main():
    config = get_config()
    
    print("=== Configuration ===")
    print(f"API Key: {'[SET]' if config.api_key else '[NOT SET]'}")
    print(f"Output Dir: {config.output_dir}")
    print(f"Log Level: {config.log_level}")

if __name__ == "__main__":
    main()