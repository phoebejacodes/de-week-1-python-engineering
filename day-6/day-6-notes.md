# Day 6: Data Formats: Parquet Fundamentals

### Overview:

Apache parquet is an open-source file format that provides efficient storage and fast read speed. It uses a hybrid storage format which sequentially stores chunks of columns, lending to high performance when selecting and filtering data. On top of strong compression algorithm support (snappy, gzip, LZO), it also provides some clever tricks for reducing file scans and encoding repeat variables.

---
## What Is Columnar Storage?
Columnar storage organizes data **by column instead of by row**.

- Traditional row-based storage (CSV, relational rows):
  - Stores entire rows together.
  - Good for reading whole records.
  - Inefficient for analytics that read only a few columns.

- Columnar storage (ORC):
 - Extremely fast for analytics
 - Harder to reconstruct rows
 - Less flexible for mixed workloads

- Parquet (Hybrid)
 - Reads only the columns you need
 - Still preserves row grouping for joins and filters
 - Stores rich metadata (min/max, statistics)
 - Optimized for distributed systems (Spark, BigQuery, Snowflake)

**Key idea:**  
If you only need 3 columns out of 100, a columnar format reads *only those 3 columns*, not the entire dataset.

**Parquet** Data is stored column-by-column. But grouped into row groups so related rows stay close together.
---

## Why Parquet Is Smaller Than CSV

Parquet achieves much smaller file sizes due to:

### 1. Column-Based Compression
- Similar values are stored together.
- Compression algorithms work better on repeated or similar data.
- Example: a column of country codes compresses extremely well.

### 2. Encoding Techniques
- Dictionary encoding (replaces repeated values with small integers)
- Run-length encoding (stores repeated values as value + count)
- Bit-packing (uses only required bits per value)

### 3. Binary Format (Not Text)
- CSV stores everything as text.
- Parquet stores data in binary form, which is more compact and faster to parse.

**Result:**  
Parquet files are often **5–10× smaller** than CSV.

---

## Why Parquet Is Faster for Analytics

### 1. Column Pruning
Only the columns referenced in a query are read from disk.

Example:
```sql
SELECT price FROM sales;
```
Only the price column is loaded, not the entire row.

### 2. Predicate Pushdown

Filters (e.g., WHERE country = 'US') are applied before reading data.
Entire blocks of data are skipped if they don’t match.

### 3. Row Group Metadata

Each Parquet file stores metadata (min/max values per block), allowing the engine to skip irrelevant chunks entirely.

### 4. Optimized for Parallel Processing

Parquet files can be split across workers, enabling fast parallel reads in Spark, Snowflake, BigQuery, etc.
---


Summary Table

| Feature               | CSV       | Parquet           |
| --------------------- | --------- | ----------------- |
| Storage format        | Row-based | Hybrid            |
| File size             | Large     | Much smaller      |
| Compression           | None      | Built-in          |
| Read speed            | Slow      | Fast              |
| Schema support        | Weak      | Strong            |
| Analytics performance | Poor      | Excellent         |
| Cloud / big data use  | Not ideal | Industry standard |



### Key Concepts

Parquet trades human readability for speed, compression, and scalability — exactly what data engineering systems need.
Data engineers work with many formats:

CSV (simple, universal, slow)
JSON (flexible, human-readable, verbose)
Parquet (columnar, compressed, fast)

| Format  | Think of it as        | Good for                          | Bad for                    |
|--------|----------------------|-----------------------------------|----------------------------|
| CSV    | A spreadsheet         | Simple data, quick inspection     | Large datasets, schemas    |
| JSON   | Nested documents      | APIs, configs, semi-structured data | Analytics, large datasets |
| Parquet| Columnar binary format| Analytics, big data workloads     | Human readability          |

| Feature                | CSV                       | JSON                  | Parquet                      |
| ---------------------- | ------------------------- | --------------------- | ---------------------------- |
| **Data Structure**     | Row-based                 | Hierarchical (nested) | Columnar (hybrid)            |
| **Human Readable**     | ✅ Very                    | ✅ Yes                 | ❌ No                         |
| **Schema**             | Implicit                  | Semi-structured       | Strongly typed               |
| **Compression**        | ❌ None                    | ⚠️ Limited            | ✅ Excellent                  |
| **File Size**          | Large                     | Medium                | Very small                   |
| **Read Performance**   | Slow                      | Moderate              | Very fast                    |
| **Write Performance**  | Fast                      | Moderate              | Slower (optimized for reads) |
| **Column Pruning**     | ❌ No                      | ❌ No                  | ✅ Yes                        |
| **Schema Evolution**   | ❌ Manual                  | ⚠️ Partial            | ✅ Supported                  |
| **Analytics Friendly** | ❌ Poor                    | ⚠️ Medium             | ✅ Excellent                  |
| **Best Use Case**      | Simple exports, debugging | APIs, configs, logs   | Data lakes, analytics, ML    |
| **Used By**            | Excel, basic tools        | APIs, NoSQL systems   | Spark, Snowflake, BigQuery   |

### 01_csv_deep_dive.py
**Key insight:** CSV stores everything as strings. You must convert types manually.

### 02_json_deep_dive.py
**Key insights:**
- JSON preserves types (integers stay integers) and suports nesting.
- JSON Lines (.jsonl) is better for streaming large files
- Pretty printing increases file size significantly
| Format      | File Size | Read Speed | Use Case                   |
| ----------- | --------- | ---------- | -------------------------- |
| JSON        | Medium    | Medium     | APIs, configs              |
| Pretty JSON | Large     | Slower     | Debugging, learning        |
| JSON Lines  | Small     | Fast       | Streaming, logs, pipelines |

### 03_parquet_intro.py, 04_parquet_advanced.py
**Key insights:**
- Parquet is significantly smaller
- Types are preserved automatically
- Reading is fast
| Concept                          | What You Learned                     |
| -------------------------------- | ------------------------------------ |
| Schema enforcement               | Data structure matters               |
| Columnar layout                  | Enables fast analytics               |
| Compression                      | Saves storage + improves performance |
| Predicate pushdown               | Avoids reading unnecessary data      |
| Separation of storage vs compute | Foundation of modern data platforms  |

### 06_format_converter.py
A universal file converter capable of reading and writing multiple data formats (CSV, JSON, JSONL, Parquet) using a single, clean interface.

This exercise ties together:
- File I/O
- Schema awareness
- Format detection
- Performance tradeoffs
- Real-world data engineering patterns

### 09_data_format_pipeline.py

Complete Data Format Pipeline — Final Exercise
What this tool does

✔ Reads CSV / JSON / JSONL / Parquet
✔ Filters rows (--filter "value > 100")
✔ Selects columns (--columns id,name)
✔ Writes to any supported format
✔ Shows useful stats
✔ Uses safe, scalable patterns

┌─────────────────────────────┐
│ 1. CLI Arguments            │  ← argparse
└────────────┬────────────────┘
             ↓
┌─────────────────────────────┐
│ 2. Read Data (CSV/JSON/etc) │  ← pandas / pyarrow
└────────────┬────────────────┘
             ↓
┌─────────────────────────────┐
│ 3. Transform                │
│   - filter rows             │
│   - select columns          │
└────────────┬────────────────┘
             ↓
┌─────────────────────────────┐
│ 4. Write Output             │
│   - CSV / JSON / Parquet    │
└────────────┬────────────────┘
             ↓
┌─────────────────────────────┐
│ 5. Stats + Logging          │
└─────────────────────────────┘





