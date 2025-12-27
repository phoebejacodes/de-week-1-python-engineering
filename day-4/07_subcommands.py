import argparse
import json
from pathlib import Path
from datetime import datetime

def cmd_fetch(args):
    """Handle fetch subcommand"""
    print(f"Fetching weather for: {args.cities}")
    print(f"Output: {args.output}")
    print(f"Verbose: {args.verbose}")
    # In real code, you'd call the API here

def cmd_convert(args):
    """Handle convert subcommand"""
    print(f"Converting: {args.input}")
    print(f"To format: {args.format}")
    print(f"Output: {args.output}")
    # In real code, you'd do the conversion here

def cmd_list(args):
    """Handle list subcommand"""
    output_dir = Path(args.directory)
    if not output_dir.exists():
        print(f"Directory not found: {output_dir}")
        return
    
    files = list(output_dir.glob("*.json")) + list(output_dir.glob("*.csv"))
    print(f"Files in {output_dir}:")
    for f in files:
        size = f.stat().st_size
        print(f"  {f.name} ({size} bytes)")

def main():
    # Main parser
    parser = argparse.ArgumentParser(
        description="Weather data management tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Create subparsers
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Fetch subcommand
    fetch_parser = subparsers.add_parser("fetch", help="Fetch weather data")
    fetch_parser.add_argument("cities", help="Comma-separated cities")
    fetch_parser.add_argument("--output", "-o", default="weather.json")
    fetch_parser.add_argument("--verbose", "-v", action="store_true")
    fetch_parser.set_defaults(func=cmd_fetch)
    
    # Convert subcommand
    convert_parser = subparsers.add_parser("convert", help="Convert data format")
    convert_parser.add_argument("input", help="Input file")
    convert_parser.add_argument("--format", "-f", choices=["json", "csv"], required=True)
    convert_parser.add_argument("--output", "-o", required=True)
    convert_parser.set_defaults(func=cmd_convert)
    
    # List subcommand
    list_parser = subparsers.add_parser("list", help="List output files")
    list_parser.add_argument("--directory", "-d", default="output")
    list_parser.set_defaults(func=cmd_list)
    
    # Parse and execute
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return 1
    
    args.func(args)
    return 0

if __name__ == "__main__":
    exit(main())