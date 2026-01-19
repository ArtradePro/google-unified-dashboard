"""
Data aggregation and processing utilities
"""

from datetime import datetime, timezone
from typing import Dict, List
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class DataAggregator:
    """Aggregates and processes usage data from multiple sources"""
    
    def __init__(self, config: Dict):
        """Initialize the aggregator with configuration"""
        self.config = config
        self.cost_mapping = config.get('cost_mapping', {})
        
    def aggregate(self, raw_data: List[Dict]) -> List[Dict]:
        """
        Aggregate raw data from multiple sources
        
        Args:
            raw_data: List of raw data records from collectors
            
        Returns:
            List of aggregated and enriched data records
        """
        aggregated = []
        
        for record in raw_data:
            try:
                enriched_record = self._enrich_record(record)
                aggregated.append(enriched_record)
            except Exception as e:
                logger.error(f"Error processing record: {e}")
                continue
                
        return aggregated
        
    def _enrich_record(self, record: Dict) -> Dict:
        """
        Enrich a single record with calculated costs and metadata
        
        Args:
            record: Raw data record
            
        Returns:
            Enriched record with cost calculations
        """
        enriched = record.copy()
        
        # Add timestamp if not present
        if 'timestamp' not in enriched:
            enriched['timestamp'] = datetime.now(timezone.utc).isoformat()
            
        # Calculate cost based on usage
        service = enriched.get('service', '')
        if service in self.cost_mapping:
            enriched['calculated_cost'] = self._calculate_cost(enriched)
        else:
            enriched['calculated_cost'] = 0.0
            
        return enriched
        
    def _calculate_cost(self, record: Dict) -> float:
        """
        Calculate cost for a record based on usage metrics
        
        Args:
            record: Data record with usage metrics
            
        Returns:
            Calculated cost in USD
        """
        service = record.get('service', '')
        cost_config = self.cost_mapping.get(service, {})
        total_cost = 0.0
        
        # Calculate based on available metrics
        for metric, value in record.items():
            if metric in cost_config and isinstance(value, (int, float)):
                rate = cost_config[metric]
                total_cost += value * rate
                
        return round(total_cost, 4)
