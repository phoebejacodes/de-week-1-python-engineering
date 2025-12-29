"""Data format handling"""

import json
import csv
from os import path
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class DataWriter:
    """Write data to various formats"""
    
    SUPPORTED_FORMATS = ["json", "csv", "parquet", "jsonl"]
    
    @staticmethod
    def write(data: List[Dict[str, Any]], path: Path, format: str = None):
        """Write data to file in specified format"""
        path = Path(path)
        format = format or path.suffix.lstrip(".")
        
        if format not in DataWriter.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {format}")
        
        path.parent.mkdir(parents=True, exist_ok=True)
        
        writer_func = getattr(DataWriter, f"_write_{format}")
        writer_func(data, path)
        
        logger.info(f"Wrote {len(data)} records to {path}")
    
    @staticmethod
    def _write_json(data: List[Dict], path: Path):
        path.write_text(json.dumps(data, indent=2))
    
    @staticmethod
    def _write_jsonl(data: List[Dict], path: Path):
        with open(path, "w") as f:
            for record in data:
                f.write(json.dumps(record) + "\n")
    
    @staticmethod
    def _write_csv(data: List[Dict], path: Path):
        if not data:
            return
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    
    @staticmethod
    def _write_parquet(data: List[Dict], path: Path):
        if not data:
            return
        df = pd.DataFrame(data)
        df.to_parquet(path, index=False)

class DataReader:
    """Read data from various formats"""
    
    SUPPORTED_FORMATS = ["json", "csv", "parquet", "jsonl"]
    
    @staticmethod
    def read(path: Path, format: str = None) -> List[Dict[str, Any]]:
        """Read data from file"""
        path = Path(path)
        format = format or path.suffix.lstrip(".")
        
        if format not in DataReader.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {format}")
        
        reader_func = getattr(DataReader, f"_read_{format}")
        data = reader_func(path)
        
        logger.info(f"Read {len(data)} records from {path}")
        return data
    
    @staticmethod
    def _read_json(path: Path) -> List[Dict]:
        data = json.loads(path.read_text())
    
    # Handle wrapped format
        if isinstance(data, dict) and "data" in data:
                return data["data"]
    
        return data

    
    @staticmethod
    def _read_jsonl(path: Path) -> List[Dict]:
        records = []
        with open(path) as f:
            for line in f:
                records.append(json.loads(line))
        return records
    
    @staticmethod
    def _read_csv(path: Path) -> List[Dict]:
        with open(path) as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    @staticmethod
    def _read_parquet(path: Path) -> List[Dict]:
        df = pd.read_parquet(path)
        return df.to_dict(orient="records")