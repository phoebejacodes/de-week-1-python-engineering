import argparse
import pandas as pd
import pyarrow.parquet as pq
from pathlib import Path
import json
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

SUPPORTED_FORMATS = {"csv", "json", "jsonl", "parquet"}

# ---------- Helpers ----------

def read_data(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower().lstrip(".")
    logger.info(f"Reading {suffix} file")

    if suffix == "csv":
        return pd.read_csv(path)
    elif suffix == "json":
        return pd.read_json(path)
    elif suffix == "jsonl":
        return pd.read_json(path, lines=True)
    elif suffix == "parquet":
        return pd.read_parquet(path)
    else:
        raise ValueError(f"Unsupported format: {suffix}")

def write_data(df: pd.DataFrame, path: Path):
    suffix = path.suffix.lower().lstrip(".")
    logger.info(f"Writing {suffix} file")

    if suffix == "csv":
        df.to_csv(path, index=False)
    elif suffix == "json":
        df.to_json(path, orient="records", indent=2)
    elif suffix == "jsonl":
        df.to_json(path, orient="records", lines=True)
    elif suffix == "parquet":
        df.to_parquet(path, index=False)
    else:
        raise ValueError(f"Unsupported output format: {suffix}")

def apply_filter(df: pd.DataFrame, filter_expr: str):
    """Example: 'value > 100'"""
    logger.info(f"Applying filter: {filter_expr}")
    return df.query(filter_expr)

def select_columns(df: pd.DataFrame, columns: str):
    cols = [c.strip() for c in columns.split(",")]
    return df[cols]

# ---------- Main CLI ----------

def main():
    parser = argparse.ArgumentParser(description="Universal Data Format Converter")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--filter", help="Row filter (e.g. value > 100)")
    parser.add_argument("--columns", help="Comma-separated column list")
    parser.add_argument("--stats", action="store_true", help="Show dataset stats")

    args = parser.parse_args()

    start = time.time()

    # Load
    df = read_data(args.input)

    # Transform
    if args.filter:
        df = apply_filter(df, args.filter)

    if args.columns:
        df = select_columns(df, args.columns)

    # Output
    write_data(df, args.output)

    # Stats
    elapsed = time.time() - start
    print("\n=== Conversion Summary ===")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Time: {elapsed:.2f}s")
    print(f"Output: {args.output}")

    if args.stats:
        print("\n=== Column Types ===")
        print(df.dtypes)

if __name__ == "__main__":
    main()
