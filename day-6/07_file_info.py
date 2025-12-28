import argparse
import pandas as pd
import pyarrow.parquet as pq
import json
from pathlib import Path

def get_csv_info(path: Path) -> dict:
    df = pd.read_csv(path, nrows=5)
    total_rows = sum(1 for _ in open(path)) - 1  # Minus header
    
    return {
        "format": "CSV",
        "rows": total_rows,
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "size_bytes": path.stat().st_size,
        "sample": df.head().to_dict(orient="records")
    }

def get_json_info(path: Path) -> dict:
    with open(path) as f:
        data = json.load(f)
    
    if isinstance(data, list):
        rows = len(data)
        columns = list(data[0].keys()) if data else []
        sample = data[:5]
    else:
        rows = 1
        columns = list(data.keys())
        sample = [data]
    
    return {
        "format": "JSON",
        "rows": rows,
        "columns": len(columns),
        "column_names": columns,
        "size_bytes": path.stat().st_size,
        "sample": sample
    }

def get_parquet_info(path: Path) -> dict:
    pf = pq.ParquetFile(path)
    metadata = pf.metadata
    schema = pf.schema_arrow
    
    df = pd.read_parquet(path, columns=None).head()
    
    return {
        "format": "Parquet",
        "rows": metadata.num_rows,
        "columns": metadata.num_columns,
        "column_names": [field.name for field in schema],
        "column_types": {field.name: str(field.type) for field in schema},
        "row_groups": metadata.num_row_groups,
        "size_bytes": path.stat().st_size,
        "compression": pf.metadata.row_group(0).column(0).compression,
        "sample": df.to_dict(orient="records")
    }

def get_file_info(path: Path) -> dict:
    suffix = path.suffix.lower()
    
    if suffix == ".csv":
        return get_csv_info(path)
    elif suffix == ".json":
        return get_json_info(path)
    elif suffix == ".parquet":
        return get_parquet_info(path)
    else:
        raise ValueError(f"Unsupported format: {suffix}")

def main():
    parser = argparse.ArgumentParser(description="Get info about data files")
    parser.add_argument("file", type=Path, help="File to inspect")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    if not args.file.exists():
        print(f"File not found: {args.file}")
        return 1
    
    info = get_file_info(args.file)
    
    if args.json:
        print(json.dumps(info, indent=2, default=str))
    else:
        print(f"\n=== File Info: {args.file.name} ===")
        print(f"Format: {info['format']}")
        print(f"Rows: {info['rows']:,}")
        print(f"Columns: {info['columns']}")
        print(f"Size: {info['size_bytes']:,} bytes")
        print(f"\nColumn names: {', '.join(info['column_names'])}")
        
        if 'column_types' in info:
            print(f"\nColumn types:")
            for col, dtype in info['column_types'].items():
                print(f"  {col}: {dtype}")
        
        if 'compression' in info:
            print(f"\nCompression: {info['compression']}")
        
        print(f"\nSample data:")
        for i, row in enumerate(info['sample'][:3]):
            print(f"  Row {i}: {row}")
    
    return 0

if __name__ == "__main__":
    exit(main())