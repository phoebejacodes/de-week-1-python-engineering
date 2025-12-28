import json
from pathlib import Path
import time

# Create sample data
data = [
    {"id": i, "name": f"User_{i}", "value": i * 1.5, "active": i % 2 == 0}
    for i in range(10000)
]

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# Write JSON - standard
print("=== Writing JSON (standard) ===")
start = time.time()

with open(output_dir / "standard.json", "w") as f:
    json.dump(data, f)

json_time = time.time() - start
json_size = (output_dir / "standard.json").stat().st_size
print(f"Time: {json_time:.3f}s")
print(f"Size: {json_size:,} bytes")

# Write JSON - pretty
print("\n=== Writing JSON (pretty) ===")
start = time.time()

with open(output_dir / "pretty.json", "w") as f:
    json.dump(data, f, indent=2)

pretty_time = time.time() - start
pretty_size = (output_dir / "pretty.json").stat().st_size
print(f"Time: {pretty_time:.3f}s")
print(f"Size: {pretty_size:,} bytes")
print(f"Pretty is {pretty_size / json_size:.1f}x larger!")

# Write JSON Lines (one JSON object per line)
print("\n=== Writing JSON Lines ===")
start = time.time()

with open(output_dir / "data.jsonl", "w") as f:
    for row in data:
        f.write(json.dumps(row) + "\n")

jsonl_time = time.time() - start
jsonl_size = (output_dir / "data.jsonl").stat().st_size
print(f"Time: {jsonl_time:.3f}s")
print(f"Size: {jsonl_size:,} bytes")

# Read JSON
print("\n=== Reading JSON ===")
start = time.time()

with open(output_dir / "standard.json", "r") as f:
    loaded = json.load(f)

read_time = time.time() - start
print(f"Time: {read_time:.3f}s")
print(f"Rows: {len(loaded)}")
print(f"Type of 'id': {type(loaded[0]['id'])}")  # Types preserved!
print(f"Type of 'value': {type(loaded[0]['value'])}")

# Read JSON Lines (streaming - memory efficient)
print("\n=== Reading JSON Lines (streaming) ===")
start = time.time()

rows = []
with open(output_dir / "data.jsonl", "r") as f:
    for line in f:
        rows.append(json.loads(line))

jsonl_read_time = time.time() - start
print(f"Time: {jsonl_read_time:.3f}s")
print(f"Rows: {len(rows)}")