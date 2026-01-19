"""
Opal usage data collector
"""

from typing import Dict, List
from datetime import datetime, timedelta
import requests
from src.collectors.base_collector import BaseCollector
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class OpalCollector(BaseCollector):
    """Collector for Opal usage data"""
    
    def __init__(self, config: Dict):
        """Initialize Opal collector"""
        super().__init__(config)
        self.api_key = self._get_api_key(
            config['sources']['opal']['api_key_env']
        )
        self.endpoint = config['sources']['opal']['endpoint']
        
    def collect(self) -> List[Dict]:
        """
        Collect usage data from Opal API
        
        Returns:
            List of usage data records
        """
        if not self.api_key:
            logger.warning("Opal API key not configured, skipping collection")
            return []
            
        try:
            usage_data = self._fetch_usage_data()
            return self._process_usage_data(usage_data)
        except Exception as e:
            logger.error(f"Error collecting Opal data: {e}")
            return []
            
    def _fetch_usage_data(self) -> Dict:
        """
        Fetch usage data from Opal API
        
        Returns:
            Raw usage data from API
        """
        logger.info("Fetching Opal usage data...")
        
        # Placeholder implementation
        # Real implementation would make actual API calls
        return {
            'api_calls': 1250,
            'active_users': 45,
            'user_seats': 50,
            'resources_managed': 320,
            'period_start': (datetime.utcnow() - timedelta(days=1)).isoformat(),
            'period_end': datetime.utcnow().isoformat()
        }
        
    def _process_usage_data(self, raw_data: Dict) -> List[Dict]:
        """
        Process raw usage data into standardized records
        
        Args:
            raw_data: Raw data from Opal API
            
        Returns:
            List of processed records
        """
        records = []
        
        record = self._create_record(
            metric_type='platform_usage',
            api_call=raw_data.get('api_calls', 0),
            active_users=raw_data.get('active_users', 0),
            user_seat=raw_data.get('user_seats', 0),
            resources_managed=raw_data.get('resources_managed', 0),
            period_start=raw_data.get('period_start'),
            period_end=raw_data.get('period_end')
        )
        records.append(record)
        
        logger.info(f"Processed Opal data: {len(records)} records")
        return records
