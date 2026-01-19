"""
Google Unified Dashboard - Main Application
Aggregates usage data from multiple Google and AI tools into Google Sheets
"""

import os
import sys
from typing import Dict, List
import yaml
from dotenv import load_dotenv

from src.collectors.gemini_collector import GeminiCollector
from src.collectors.opal_collector import OpalCollector
from src.collectors.wisk_collector import WiskCollector
from src.collectors.polemi_collector import PolemiCollector
from src.integrations.sheets_integration import SheetsIntegration
from src.utils.aggregator import DataAggregator
from src.utils.logger import setup_logger

# Load environment variables
load_dotenv()

logger = setup_logger(__name__)


class UnifiedDashboard:
    """Main application class for aggregating usage data"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the dashboard with configuration"""
        self.config = self._load_config(config_path)
        self.sheets = SheetsIntegration(self.config)
        self.aggregator = DataAggregator(self.config)
        self.collectors = self._initialize_collectors()
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_path}")
            sys.exit(1)
        except yaml.YAMLError as e:
            logger.error(f"Error parsing configuration file: {e}")
            sys.exit(1)
            
    def _initialize_collectors(self) -> Dict:
        """Initialize data collectors for each service"""
        collectors = {}
        
        sources = self.config.get('sources', {})
        
        if sources.get('gemini', {}).get('enabled', False):
            collectors['gemini'] = GeminiCollector(self.config)
            
        if sources.get('opal', {}).get('enabled', False):
            collectors['opal'] = OpalCollector(self.config)
            
        if sources.get('wisk', {}).get('enabled', False):
            collectors['wisk'] = WiskCollector(self.config)
            
        if sources.get('polemi', {}).get('enabled', False):
            collectors['polemi'] = PolemiCollector(self.config)
            
        logger.info(f"Initialized {len(collectors)} collectors: {', '.join(collectors.keys())}")
        return collectors
        
    def collect_usage_data(self) -> List[Dict]:
        """Collect usage data from all enabled sources"""
        all_data = []
        
        for name, collector in self.collectors.items():
            try:
                logger.info(f"Collecting data from {name}...")
                data = collector.collect()
                if data:
                    all_data.extend(data)
                    logger.info(f"Collected {len(data)} records from {name}")
                else:
                    logger.warning(f"No data collected from {name}")
            except Exception as e:
                logger.error(f"Error collecting data from {name}: {e}")
                
        return all_data
        
    def process_and_aggregate(self, raw_data: List[Dict]) -> List[Dict]:
        """Process and aggregate collected data"""
        logger.info("Processing and aggregating data...")
        aggregated = self.aggregator.aggregate(raw_data)
        logger.info(f"Aggregated {len(aggregated)} records")
        return aggregated
        
    def write_to_sheets(self, data: List[Dict]):
        """Write aggregated data to Google Sheets"""
        logger.info("Writing data to Google Sheets...")
        self.sheets.write_data(data)
        logger.info("Data successfully written to Google Sheets")
        
    def run(self):
        """Main execution method"""
        logger.info("=" * 60)
        logger.info("Starting Google Unified Dashboard data collection")
        logger.info("=" * 60)
        
        try:
            # Collect data from all sources
            raw_data = self.collect_usage_data()
            
            if not raw_data:
                logger.warning("No data collected from any source")
                return
                
            # Process and aggregate data
            aggregated_data = self.process_and_aggregate(raw_data)
            
            # Write to Google Sheets
            self.write_to_sheets(aggregated_data)
            
            logger.info("=" * 60)
            logger.info("Data collection and aggregation completed successfully")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"Error during execution: {e}", exc_info=True)
            sys.exit(1)


def main():
    """Entry point for the application"""
    dashboard = UnifiedDashboard()
    dashboard.run()


if __name__ == "__main__":
    main()
