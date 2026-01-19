"""
Base collector class for all data collectors
"""

from abc import ABC, abstractmethod
from typing import Dict, List
from datetime import datetime, timezone
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class BaseCollector(ABC):
    """Abstract base class for data collectors"""
    
    def __init__(self, config: Dict):
        """
        Initialize the collector with configuration
        
        Args:
            config: Application configuration dictionary
        """
        self.config = config
        self.service_name = self.__class__.__name__.replace('Collector', '').lower()
        
    @abstractmethod
    def collect(self) -> List[Dict]:
        """
        Collect usage data from the service
        
        Returns:
            List of usage data records
        """
        pass
        
    def _get_api_key(self, key_env: str) -> str:
        """
        Get API key from environment variable
        
        Args:
            key_env: Name of the environment variable
            
        Returns:
            API key value
        """
        import os
        api_key = os.getenv(key_env)
        if not api_key:
            logger.warning(f"API key not found for {key_env}")
        return api_key
        
    def _create_record(self, **kwargs) -> Dict:
        """
        Create a standardized data record
        
        Args:
            **kwargs: Record fields
            
        Returns:
            Standardized data record
        """
        record = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'service': self.service_name,
            **kwargs
        }
        return record
