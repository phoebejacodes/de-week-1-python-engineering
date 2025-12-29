"""Configuration management for the weather pipeline"""

from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class PipelineConfig:
    """Pipeline configuration"""
    
    # API
    api_key: str = field(default_factory=lambda: os.getenv("OPENWEATHER_API_KEY", ""))
    api_base_url: str = "https://api.openweathermap.org/data/2.5/weather"
    api_timeout: int = 10
    
    # Rate limiting
    calls_per_second: float = 1.0
    
    # Retry
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 30.0
    
    # Paths
    base_dir: Path = field(default_factory=lambda: Path(__file__).parent.parent)
    output_dir: Path = field(default=None)
    log_dir: Path = field(default=None)
    data_dir: Path = field(default=None)
    
    # Logging
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    
    def __post_init__(self):
        """Set up paths after initialization"""
        if self.output_dir is None:
            self.output_dir = self.base_dir / "output"
        if self.log_dir is None:
            self.log_dir = self.base_dir / "logs"
        if self.data_dir is None:
            self.data_dir = self.base_dir / "data"
        
        # Create directories
        for dir_path in [self.output_dir, self.log_dir, self.data_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def validate(self) -> bool:
        """Validate configuration"""
        if not self.api_key:
            return False
        return True

# Default config instance
config = PipelineConfig()