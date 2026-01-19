"""
Wisk usage data collector
"""

from typing import Dict, List
from datetime import datetime, timedelta, timezone
from src.collectors.base_collector import BaseCollector
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class WiskCollector(BaseCollector):
    """Collector for Wisk usage data"""
    
    def __init__(self, config: Dict):
        """Initialize Wisk collector"""
        super().__init__(config)
        self.api_key = self._get_api_key(
            config['sources']['wisk']['api_key_env']
        )
        self.endpoint = config['sources']['wisk']['endpoint']
        
    def collect(self) -> List[Dict]:
        """
        Collect usage data from Wisk API
        
        Returns:
            List of usage data records
        """
        if not self.api_key:
            logger.warning("Wisk API key not configured, skipping collection")
            return []
            
        try:
            usage_data = self._fetch_usage_data()
            return self._process_usage_data(usage_data)
        except Exception as e:
            logger.error(f"Error collecting Wisk data: {e}")
            return []
            
    def _fetch_usage_data(self) -> Dict:
        """
        Fetch usage data from Wisk API
        
        Returns:
            Raw usage data from API
        """
        logger.info("Fetching Wisk usage data...")
        
        # Placeholder implementation
        # Real implementation would make actual API calls
        return {
            'api_calls': 850,
            'storage_gb': 125.5,
            'data_transfers_gb': 45.2,
            'active_projects': 12,
            'period_start': (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
            'period_end': datetime.now(timezone.utc).isoformat()
        }
        
    def _process_usage_data(self, raw_data: Dict) -> List[Dict]:
        """
        Process raw usage data into standardized records
        
        Args:
            raw_data: Raw data from Wisk API
            
        Returns:
            List of processed records
        """
        records = []
        
        record = self._create_record(
            metric_type='platform_usage',
            api_call=raw_data.get('api_calls', 0),
            storage_gb=raw_data.get('storage_gb', 0),
            data_transfers_gb=raw_data.get('data_transfers_gb', 0),
            active_projects=raw_data.get('active_projects', 0),
            period_start=raw_data.get('period_start'),
            period_end=raw_data.get('period_end')
        )
        records.append(record)
        
        logger.info(f"Processed Wisk data: {len(records)} records")
        return records
