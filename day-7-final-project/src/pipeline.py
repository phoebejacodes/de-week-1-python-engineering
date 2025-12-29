"""Main pipeline orchestration"""

import logging
from typing import List, Optional, Dict, Any
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field

from .config import PipelineConfig
from .api import WeatherAPIClient, WeatherData
from .formats import DataWriter

logger = logging.getLogger(__name__)

@dataclass
class PipelineStats:
    """Track pipeline execution statistics"""
    total: int = 0
    success: int = 0
    failed: int = 0
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    
    @property
    def duration_seconds(self) -> float:
        end = self.end_time or datetime.now()
        return (end - self.start_time).total_seconds()
    
    @property
    def success_rate(self) -> float:
        return (self.success / self.total * 100) if self.total > 0 else 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "total": self.total,
            "success": self.success,
            "failed": self.failed,
            "success_rate": f"{self.success_rate:.1f}%",
            "duration_seconds": f"{self.duration_seconds:.2f}"
        }

class WeatherPipeline:
    """Main weather data pipeline"""
    
    def __init__(self, config: PipelineConfig = None):
        self.config = config or PipelineConfig()
        self.client = WeatherAPIClient(self.config)
        self.stats = PipelineStats()
    
    def load_cities_from_file(self, path: Path) -> List[str]:
        """Load city list from file"""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Cities file not found: {path}")
        
        cities = [
            line.strip()
            for line in path.read_text().strip().split("\n")
            if line.strip() and not line.startswith("#")
        ]
        
        logger.info(f"Loaded {len(cities)} cities from {path}")
        return cities
    
    def fetch_weather(self, cities: List[str]) -> List[WeatherData]:
        """Fetch weather for multiple cities"""
        logger.info(f"Starting pipeline for {len(cities)} cities")
        
        self.stats = PipelineStats()
        self.stats.total = len(cities)
        
        results = []
        
        for city in cities:
            weather = self.client.fetch(city)
            if weather:
                results.append(weather)
                self.stats.success += 1
            else:
                self.stats.failed += 1
        
        self.stats.end_time = datetime.now()
        
        logger.info(
            f"Pipeline complete: {self.stats.success}/{self.stats.total} "
            f"({self.stats.success_rate:.1f}%) in {self.stats.duration_seconds:.2f}s"
        )
        
        return results
    
    def save_results(
        self,
        results: List[WeatherData],
        output_path: Path,
        format: str = None,
        include_metadata: bool = True
    ):
        """Save results to file"""
        data = [r.to_dict() for r in results]
        
        if include_metadata and format in ["json", None]:
            output = {
                "metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "record_count": len(data),
                    "stats": self.stats.to_dict()
                },
                "data": data
            }
            Path(output_path).write_text(__import__("json").dumps(output, indent=2))
            logger.info(f"Saved results with metadata to {output_path}")
        else:
            DataWriter.write(data, output_path, format)
    
    def run(
        self,
        cities: List[str] = None,
        cities_file: Path = None,
        output_path: Path = None,
        output_format: str = "json"
    ) -> List[WeatherData]:
        """Run the complete pipeline"""
        # Get cities
        if cities_file:
            cities = self.load_cities_from_file(cities_file)
        elif not cities:
            raise ValueError("Must provide cities or cities_file")
        
        # Fetch data
        results = self.fetch_weather(cities)
        
        # Save if output path provided
        if output_path and results:
            self.save_results(results, output_path, output_format)
        
        return results