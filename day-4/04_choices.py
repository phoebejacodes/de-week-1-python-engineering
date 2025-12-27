import argparse

parser = argparse.ArgumentParser(description="Format converter")

parser.add_argument("input_file", help="File to convert")
parser.add_argument(
    "--format",
    choices=["json", "csv", "parquet"],
    default="json",
    help="Output format"
)
parser.add_argument(
    "--verbose", "-v",
    action="store_true",
    help="Show detailed output"
)

args = parser.parse_args()

print(f"Input: {args.input_file}")
print(f"Format: {args.format}")
print(f"Verbose: {args.verbose}")