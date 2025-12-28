import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# Create data with explicit schema
data = {
    "id": list(range(100000)),
    "name": [f"User_{i}" for i in range(100000)],
    "value": [i * 1.5 for i in range(100000)],
    "category": ["A", "B", "C", "D"] * 25000,  # Repeated values compress well
    "active": [i % 2 == 0 for i in range(100000)]
}

# Define schema explicitly
schema = pa.schema([
    ("id", pa.int64()),
    ("name", pa.string()),
    ("value", pa.float64()),
    ("category", pa.string()),
    ("active", pa.bool_())
])

# Create table with schema
table = pa.table(data, schema=schema)

print("=== Schema ===")
print(table.schema)

# Write with different compression
compressions = ["none", "snappy", "gzip", "zstd"]

print("\n=== Compression Comparison ===")
for comp in compressions:
    path = output_dir / f"data_{comp}.parquet"
    pq.write_table(table, path, compression=comp)
    size = path.stat().st_size
    print(f"{comp:>8}: {size:>12,} bytes")

# Read and inspect metadata
print("\n=== Parquet Metadata ===")
parquet_file = pq.ParquetFile(output_dir / "data_snappy.parquet")
print(f"Num rows: {parquet_file.metadata.num_rows}")
print(f"Num columns: {parquet_file.metadata.num_columns}")
print(f"Num row groups: {parquet_file.metadata.num_row_groups}")

# Read specific columns only (columnar advantage!)
print("\n=== Reading Specific Columns ===")
table_partial = pq.read_table(
    output_dir / "data_snappy.parquet",
    columns=["id", "value"]
)
print(f"Columns read: {table_partial.column_names}")
print(f"Memory usage: {table_partial.nbytes:,} bytes")

# Read with filter (predicate pushdown)
print("\n=== Reading with Filter ===")
table_filtered = pq.read_table(
    output_dir / "data_snappy.parquet",
    filters=[("id", "<", 100)]
)
print(f"Rows after filter: {table_filtered.num_rows}")