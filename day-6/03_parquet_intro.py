import pyarrow as pa
import pyarrow.parquet as pq
import json
from pathlib import Path
import time

# Create sample data
data = [
    {"id": i, "name": f"User_{i}", "value": i * 1.5, "active": i % 2 == 0}
    for i in range(100000)  # 100k rows
]

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# First, write CSV and JSON for comparison
print("=== Writing CSV ===")
start = time.time()
import csv
with open(output_dir / "data.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
csv_time = time.time() - start
csv_size = (output_dir / "data.csv").stat().st_size
print(f"Time: {csv_time:.3f}s, Size: {csv_size:,} bytes")

print("\n=== Writing JSON ===")
start = time.time()
with open(output_dir / "data.json", "w") as f:
    json.dump(data, f)
json_time = time.time() - start
json_size = (output_dir / "data.json").stat().st_size
print(f"Time: {json_time:.3f}s, Size: {json_size:,} bytes")

# Now Parquet
print("\n=== Writing Parquet ===")
start = time.time()

# Convert to PyArrow Table
table = pa.Table.from_pylist(data)

# Write to Parquet
pq.write_table(table, output_dir / "data.parquet")

parquet_time = time.time() - start
parquet_size = (output_dir / "data.parquet").stat().st_size
print(f"Time: {parquet_time:.3f}s, Size: {parquet_size:,} bytes")

# Comparison
print("\n=== Size Comparison ===")
print(f"CSV:     {csv_size:>12,} bytes (baseline)")
print(f"JSON:    {json_size:>12,} bytes ({json_size/csv_size:.2f}x CSV)")
print(f"Parquet: {parquet_size:>12,} bytes ({parquet_size/csv_size:.2f}x CSV)")
print(f"\nParquet is {csv_size/parquet_size:.1f}x smaller than CSV!")

# Read Parquet
print("\n=== Reading Parquet ===")
start = time.time()

table = pq.read_table(output_dir / "data.parquet")
df = table.to_pandas()

read_time = time.time() - start
print(f"Time: {read_time:.3f}s")
print(f"Rows: {len(df)}")
print(f"Columns: {list(df.columns)}")
print(f"\nData types:")
print(df.dtypes)
print(f"\nSample:")
print(df.head())