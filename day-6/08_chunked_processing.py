import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def create_large_csv(path: Path, rows: int = 500000):
    """Create a large CSV file for testing"""
    logger.info(f"Creating {rows:,} row CSV file...")
    
    chunks = rows // 10000
    
    with open(path, "w") as f:
        f.write("id,name,value,category\n")
        for chunk in range(chunks):
            for i in range(10000):
                row_id = chunk * 10000 + i
                f.write(f"{row_id},User_{row_id},{row_id * 1.5},{['A','B','C','D'][row_id % 4]}\n")
            if (chunk + 1) % 10 == 0:
                logger.info(f"  Created {(chunk + 1) * 10000:,} rows")
    
    logger.info(f"Created {path} ({path.stat().st_size:,} bytes)")

def process_csv_chunked(input_path: Path, output_path: Path, chunk_size: int = 50000):
    """Process large CSV in chunks and write to Parquet"""
    logger.info(f"Processing {input_path} in chunks of {chunk_size:,}")
    
    # Process in chunks
    writer = None
    total_rows = 0
    
    for i, chunk in enumerate(pd.read_csv(input_path, chunksize=chunk_size)):
        # Convert to PyArrow Table
        table = pa.Table.from_pandas(chunk)
        
        # Initialize writer on first chunk
        if writer is None:
            writer = pq.ParquetWriter(output_path, table.schema)
        
        # Write chunk
        writer.write_table(table)
        total_rows += len(chunk)
        logger.info(f"  Processed chunk {i+1}: {total_rows:,} rows total")
    
    writer.close()
    logger.info(f"Wrote {total_rows:,} rows to {output_path}")
    logger.info(f"Output size: {output_path.stat().st_size:,} bytes")

def read_parquet_chunked(path: Path, batch_size: int = 50000):
    """Read Parquet file in batches"""
    logger.info(f"Reading {path} in batches")
    
    parquet_file = pq.ParquetFile(path)
    total_rows = 0
    
    for batch in parquet_file.iter_batches(batch_size=batch_size):
        df = batch.to_pandas()
        total_rows += len(df)
        
        # Process batch here
        avg_value = df["value"].mean()
        logger.info(f"  Batch: {len(df):,} rows, avg value: {avg_value:.2f}")
    
    logger.info(f"Total rows processed: {total_rows:,}")

# Main
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# Create test file
large_csv = output_dir / "large_data.csv"
if not large_csv.exists():
    create_large_csv(large_csv, rows=500000)

# Process chunked
print("\n=== Chunked CSV to Parquet ===")
start = time.time()
process_csv_chunked(large_csv, output_dir / "large_data.parquet")
print(f"Time: {time.time() - start:.2f}s")

# Read chunked
print("\n=== Chunked Parquet Reading ===")
start = time.time()
read_parquet_chunked(output_dir / "large_data.parquet")
print(f"Time: {time.time() - start:.2f}s")

# Compare sizes
print("\n=== Size Comparison ===")
csv_size = large_csv.stat().st_size
parquet_size = (output_dir / "large_data.parquet").stat().st_size
print(f"CSV: {csv_size:,} bytes")
print(f"Parquet: {parquet_size:,} bytes")
print(f"Compression ratio: {csv_size / parquet_size:.1f}x")