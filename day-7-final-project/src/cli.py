"""Command-line interface"""

import argparse
import logging
import sys
from pathlib import Path
from datetime import datetime

from .config import PipelineConfig
from .pipeline import WeatherPipeline
from .formats import DataReader, DataWriter

def setup_logging(verbose: bool, log_dir: Path):
    """Configure logging"""
    level = logging.DEBUG if verbose else logging.INFO
    
    # Create handlers
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    
    log_file = log_dir / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    return log_file

def cmd_fetch(args):
    """Handle fetch command"""
    config = PipelineConfig()
    
    if not config.validate():
        print("Error: OPENWEATHER_API_KEY not set")
        return 1
    
    log_file = setup_logging(args.verbose, config.log_dir)
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 50)
    logger.info("Weather Pipeline - Fetch Command")
    logger.info("=" * 50)
    
    pipeline = WeatherPipeline(config)
    
    try:
        # Get cities
        if args.cities:
            cities = [c.strip() for c in args.cities.split(",")]
        elif args.file:
            cities = pipeline.load_cities_from_file(args.file)
        else:
            print("Error: Must provide --cities or --file")
            return 1
        
        # Run pipeline
        results = pipeline.fetch_weather(cities)
        
        # Save results
        if results:
            output_path = Path(args.output)
            pipeline.save_results(results, output_path, args.format)
            
            print(f"\n✓ Saved {len(results)} records to {output_path}")
        else:
            print("\n✗ No data to save")
            return 1
        
        # Print stats
        print(f"\n=== Statistics ===")
        for key, value in pipeline.stats.to_dict().items():
            print(f"  {key}: {value}")
        
        print(f"\nLog file: {log_file}")
        return 0
        
    except Exception as e:
        logger.exception(f"Pipeline failed: {e}")
        return 1

def cmd_convert(args):
    """Handle convert command"""
    logger = logging.getLogger(__name__)
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return 1
    
    try:
        data = DataReader.read(input_path)
        DataWriter.write(data, output_path, args.format)
        
        print(f"✓ Converted {len(data)} records")
        print(f"  Input: {input_path} ({input_path.stat().st_size:,} bytes)")
        print(f"  Output: {output_path} ({output_path.stat().st_size:,} bytes)")
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

def cmd_info(args):
    """Handle info command"""
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        return 1
    
    try:
        data = DataReader.read(input_path)
        
        print(f"\n=== File Info: {input_path.name} ===")
        print(f"Format: {input_path.suffix.lstrip('.')}")
        print(f"Size: {input_path.stat().st_size:,} bytes")
        print(f"Records: {len(data)}")
        
        if data:
            print(f"Columns: {', '.join(data[0].keys())}")
            print(f"\nSample (first 3 records):")
            for i, record in enumerate(data[:3]):
                print(f"  {i+1}. {record}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Weather Data Pipeline - Fetch, convert, and analyze weather data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fetch weather for specific cities
  python -m src.cli fetch --cities "London,Paris,Tokyo" --output weather.json

  # Fetch from file
  python -m src.cli fetch --file data/cities.txt --output weather.parquet --format parquet

  # Convert between formats
  python -m src.cli convert weather.json weather.csv --format csv

  # Get file info
  python -m src.cli info weather.parquet
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Fetch command
    fetch_parser = subparsers.add_parser("fetch", help="Fetch weather data")
    fetch_input = fetch_parser.add_mutually_exclusive_group(required=True)
    fetch_input.add_argument("--cities", "-c", help="Comma-separated cities")
    fetch_input.add_argument("--file", "-f", type=Path, help="File with cities")
    fetch_parser.add_argument("--output", "-o", default="output/weather.json", help="Output file")
    fetch_parser.add_argument("--format", choices=["json", "csv", "parquet", "jsonl"], default="json")
    fetch_parser.add_argument("--verbose", "-v", action="store_true")
    fetch_parser.set_defaults(func=cmd_fetch)
    
    # Convert command
    convert_parser = subparsers.add_parser("convert", help="Convert between formats")
    convert_parser.add_argument("input", type=Path, help="Input file")
    convert_parser.add_argument("output", type=Path, help="Output file")
    convert_parser.add_argument("--format", choices=["json", "csv", "parquet", "jsonl"])
    convert_parser.set_defaults(func=cmd_convert)
    
    # Info command
    info_parser = subparsers.add_parser("info", help="Show file information")
    info_parser.add_argument("input", type=Path, help="Input file")
    info_parser.set_defaults(func=cmd_info)
    
    # Parse and execute
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return 0
    
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main())