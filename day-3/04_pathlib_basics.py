from pathlib import Path

# Current directory
current = Path.cwd()
print(f"Current: {current}")

# Home directory
home = Path.home()
print(f"Home: {home}")

# Create paths
data_dir = Path("data")
output_file = data_dir / "output.csv"
print(f"Output path: {output_file}")

# Check if exists
print(f"Data dir exists: {data_dir.exists()}")

# Create directory if it doesn't exist
data_dir.mkdir(exist_ok=True)
print(f"Data dir exists now: {data_dir.exists()}")

# File operations
test_file = data_dir / "test.txt"
test_file.write_text("Hello from pathlib!")
print(f"File contents: {test_file.read_text()}")

# Get file info
print(f"File name: {test_file.name}")
print(f"File suffix: {test_file.suffix}")
print(f"File parent: {test_file.parent}")

# List files in directory
print("\nFiles in data dir:")
for file in data_dir.iterdir():
    print(f"  {file.name}")