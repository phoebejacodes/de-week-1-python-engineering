import argparse
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import json
import csv
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class FormatConverter:
    """Convert between data formats"""
    
    SUPPORTED_FORMATS = ["csv", "json", "jsonl", "parquet"]
    
    def __init__(self):
        self.readers = {
            "csv": self._read_csv,
            "json": self._read_json,
            "jsonl": self._read_jsonl,
            "parquet": self._read_parquet,
        }
        self.writers = {
            "csv": self._write_csv,
            "json": self._write_json,
            "jsonl": self._write_jsonl,
            "parquet": self._write_parquet,
        }
    
    def _read_csv(self, path: Path) -> pd.DataFrame:
        return pd.read_csv(path)
    
    def _read_json(self, path: Path) -> pd.DataFrame:
        return pd.read_json(path)
    
    def _read_jsonl(self, path: Path) -> pd.DataFrame:
        records = []
        with open(path) as f:
            for line in f:
                records.append(json.loads(line))
        return pd.DataFrame(records)
    
    def _read_parquet(self, path: Path) -> pd.DataFrame:
        return pd.read_parquet(path)
    
    def _write_csv(self, df: pd.DataFrame, path: Path):
        df.to_csv(path, index=False)
    
    def _write_json(self, df: pd.DataFrame, path: Path):
        df.to_json(path, orient="records", indent=2, date_format="iso")
    
    def _write_jsonl(self, df: pd.DataFrame, path: Path):
        with open(path, "w") as f:
            for record in df.to_dict(orient="records"):
                f.write(json.dumps(record) + "\n")
    
    def _write_parquet(self, df: pd.DataFrame, path: Path):
        df.to_parquet(path, index=False)
    
    def detect_format(self, path: Path) -> str:
        """Detect format from file extension"""
        suffix = path.suffix.lower().lstrip(".")
        if suffix in self.SUPPORTED_FORMATS:
            return suffix
        raise ValueError(f"Unsupported format: {suffix}")
    
    def convert(
        self,
        input_path: Path,
        output_path: Path,
        input_format: str = None,
        output_format: str = None
    ) -> dict:
        """Convert file from one format to another"""
        input_path = Path(input_path)
        output_path = Path(output_path)
        
        # Detect formats if not specified
        input_format = input_format or self.detect_format(input_path)
        output_format = output_format or self.detect_format(output_path)
        
        logger.info(f"Converting {input_format} -> {output_format}")
        logger.info(f"Input: {input_path}")
        logger.info(f"Output: {output_path}")
        
        # Read
        start = datetime.now()
        df = self.readers[input_format](input_path)
        read_time = (datetime.now() - start).total_seconds()
        logger.info(f"Read {len(df)} rows in {read_time:.3f}s")
        
        # Write
        output_path.parent.mkdir(parents=True, exist_ok=True)
        start = datetime.now()
        self.writers[output_format](df, output_path)
        write_time = (datetime.now() - start).total_seconds()
        logger.info(f"Wrote {len(df)} rows in {write_time:.3f}s")
        
        # Stats
        input_size = input_path.stat().st_size
        output_size = output_path.stat().st_size
        
        return {
            "input_format": input_format,
            "output_format": output_format,
            "rows": len(df),
            "columns": len(df.columns),
            "input_size": input_size,
            "output_size": output_size,
            "size_ratio": output_size / input_size,
            "read_time": read_time,
            "write_time": write_time
        }

def main():
    parser = argparse.ArgumentParser(
        description="Convert between data formats (CSV, JSON, JSONL, Parquet)"
    )
    parser.add_argument("input", type=Path, help="Input file")
    parser.add_argument("output", type=Path, help="Output file")
    parser.add_argument("--input-format", choices=FormatConverter.SUPPORTED_FORMATS)
    parser.add_argument("--output-format", choices=FormatConverter.SUPPORTED_FORMATS)
    parser.add_argument("--verbose", "-v", action="store_true")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    converter = FormatConverter()
    
    try:
        stats = converter.convert(
            args.input,
            args.output,
            args.input_format,
            args.output_format
        )
        
        print("\n=== Conversion Complete ===")
        print(f"Rows: {stats['rows']:,}")
        print(f"Columns: {stats['columns']}")
        print(f"Input size: {stats['input_size']:,} bytes")
        print(f"Output size: {stats['output_size']:,} bytes")
        print(f"Size ratio: {stats['size_ratio']:.2f}x")
        
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())