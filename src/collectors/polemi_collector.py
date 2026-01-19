"""
Polemi usage data collector
"""

from typing import Dict, List
from datetime import datetime, timedelta
import requests
from src.collectors.base_collector import BaseCollector
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class PolemiCollector(BaseCollector):
    """Collector for Polemi usage data"""
    
    def __init__(self, config: Dict):
        """Initialize Polemi collector"""
        super().__init__(config)
        self.api_key = self._get_api_key(
            config['sources']['polemi']['api_key_env']
        )
        self.endpoint = config['sources']['polemi']['endpoint']
        
    def collect(self) -> List[Dict]:
        """
        Collect usage data from Polemi API
        
        Returns:
            List of usage data records
        """
        if not self.api_key:
            logger.warning("Polemi API key not configured, skipping collection")
            return []
            
        try:
            usage_data = self._fetch_usage_data()
            return self._process_usage_data(usage_data)
        except Exception as e:
            logger.error(f"Error collecting Polemi data: {e}")
            return []
            
    def _fetch_usage_data(self) -> Dict:
        """
        Fetch usage data from Polemi API
        
        Returns:
            Raw usage data from API
        """
        logger.info("Fetching Polemi usage data...")
        
        # Placeholder implementation
        # Real implementation would make actual API calls
        return {
            'api_calls': 650,
            'compute_hours': 85.5,
            'memory_gb_hours': 340,
            'active_jobs': 28,
            'period_start': (datetime.utcnow() - timedelta(days=1)).isoformat(),
            'period_end': datetime.utcnow().isoformat()
        }
        
    def _process_usage_data(self, raw_data: Dict) -> List[Dict]:
        """
        Process raw usage data into standardized records
        
        Args:
            raw_data: Raw data from Polemi API
            
        Returns:
            List of processed records
        """
        records = []
        
        record = self._create_record(
            metric_type='compute_usage',
            api_call=raw_data.get('api_calls', 0),
            compute_hour=raw_data.get('compute_hours', 0),
            memory_gb_hours=raw_data.get('memory_gb_hours', 0),
            active_jobs=raw_data.get('active_jobs', 0),
            period_start=raw_data.get('period_start'),
            period_end=raw_data.get('period_end')
        )
        records.append(record)
        
        logger.info(f"Processed Polemi data: {len(records)} records")
        return records
