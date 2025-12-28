import csv
from pathlib import Path
import time

# Create sample data
data = [
    {"id": i, "name": f"User_{i}", "value": i * 1.5, "active": i % 2 == 0}
    for i in range(10000)
]

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# Write CSV - basic
print("=== Writing CSV (basic) ===")
start = time.time()

with open(output_dir / "basic.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

basic_time = time.time() - start
basic_size = (output_dir / "basic.csv").stat().st_size
print(f"Time: {basic_time:.3f}s")
print(f"Size: {basic_size:,} bytes")

# Read CSV - basic
print("\n=== Reading CSV (basic) ===")
start = time.time()

with open(output_dir / "basic.csv", "r") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

read_time = time.time() - start
print(f"Time: {read_time:.3f}s")
print(f"Rows: {len(rows)}")
print(f"Sample: {rows[0]}")

# Note: all values are strings!
print(f"Type of 'id': {type(rows[0]['id'])}")
print(f"Type of 'value': {type(rows[0]['value'])}")

# Reading with type conversion
print("\n=== Reading with type conversion ===")
start = time.time()

with open(output_dir / "basic.csv", "r") as f:
    reader = csv.DictReader(f)
    typed_rows = []
    for row in reader:
        typed_rows.append({
            "id": int(row["id"]),
            "name": row["name"],
            "value": float(row["value"]),
            "active": row["active"] == "True"
        })

typed_time = time.time() - start
print(f"Time: {typed_time:.3f}s")
print(f"Type of 'id': {type(typed_rows[0]['id'])}")
print(f"Type of 'value': {type(typed_rows[0]['value'])}")