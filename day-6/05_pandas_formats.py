import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
import time

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# Create DataFrame
df = pd.DataFrame({
    "id": range(100000),
    "name": [f"User_{i}" for i in range(100000)],
    "value": [i * 1.5 for i in range(100000)],
    "timestamp": pd.date_range("2024-01-01", periods=100000, freq="min")
})

print("=== DataFrame Info ===")
print(df.dtypes)
print(f"Memory usage: {df.memory_usage(deep=True).sum():,} bytes")

# Write to different formats
formats = {
    "csv": lambda p: df.to_csv(p, index=False),
    "json": lambda p: df.to_json(p, orient="records", date_format="iso"),
    "parquet": lambda p: df.to_parquet(p, index=False),
}

print("\n=== Write Performance ===")
for fmt, write_func in formats.items():
    path = output_dir / f"pandas_data.{fmt}"
    start = time.time()
    write_func(path)
    elapsed = time.time() - start
    size = path.stat().st_size
    print(f"{fmt:>8}: {elapsed:.3f}s, {size:>12,} bytes")

# Read performance
print("\n=== Read Performance ===")

start = time.time()
df_csv = pd.read_csv(output_dir / "pandas_data.csv")
print(f"CSV: {time.time() - start:.3f}s")

start = time.time()
df_json = pd.read_json(output_dir / "pandas_data.json")
print(f"JSON: {time.time() - start:.3f}s")

start = time.time()
df_parquet = pd.read_parquet(output_dir / "pandas_data.parquet")
print(f"Parquet: {time.time() - start:.3f}s")

# Type preservation
print("\n=== Type Preservation ===")
print("Original types:")
print(df.dtypes)
print("\nCSV types (types lost):")
print(df_csv.dtypes)
print("\nParquet types (types preserved):")
print(df_parquet.dtypes)