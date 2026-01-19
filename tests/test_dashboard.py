"""
Simple tests to verify the dashboard structure and functionality
"""

import sys
import os
import unittest

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.aggregator import DataAggregator
from src.collectors.base_collector import BaseCollector


class TestDataAggregator(unittest.TestCase):
    """Test the DataAggregator class"""
    
    def setUp(self):
        """Set up test configuration"""
        self.config = {
            'cost_mapping': {
                'gemini': {
                    'input_token': 0.000001,
                    'output_token': 0.000002
                },
                'opal': {
                    'api_call': 0.01,
                    'user_seat': 50.00
                }
            }
        }
        self.aggregator = DataAggregator(self.config)
        
    def test_aggregate_empty_data(self):
        """Test aggregating empty data"""
        result = self.aggregator.aggregate([])
        self.assertEqual(result, [])
        
    def test_aggregate_with_data(self):
        """Test aggregating data with records"""
        raw_data = [
            {
                'service': 'gemini',
                'input_token': 1000,
                'output_token': 500
            }
        ]
        result = self.aggregator.aggregate(raw_data)
        
        self.assertEqual(len(result), 1)
        self.assertIn('calculated_cost', result[0])
        self.assertIn('timestamp', result[0])
        
    def test_cost_calculation_gemini(self):
        """Test cost calculation for Gemini service"""
        record = {
            'service': 'gemini',
            'input_token': 100000,
            'output_token': 50000
        }
        enriched = self.aggregator._enrich_record(record)
        
        expected_cost = (100000 * 0.000001) + (50000 * 0.000002)
        self.assertAlmostEqual(enriched['calculated_cost'], expected_cost, places=4)
        
    def test_cost_calculation_opal(self):
        """Test cost calculation for Opal service"""
        record = {
            'service': 'opal',
            'api_call': 100,
            'user_seat': 10
        }
        enriched = self.aggregator._enrich_record(record)
        
        expected_cost = (100 * 0.01) + (10 * 50.00)
        self.assertEqual(enriched['calculated_cost'], expected_cost)


class MockCollector(BaseCollector):
    """Mock collector for testing"""
    
    def collect(self):
        return [
            self._create_record(
                metric_type='test',
                value=100
            )
        ]


class TestBaseCollector(unittest.TestCase):
    """Test the BaseCollector class"""
    
    def setUp(self):
        """Set up test configuration"""
        self.config = {
            'sources': {
                'test': {
                    'api_key_env': 'TEST_API_KEY'
                }
            }
        }
        
    def test_collector_initialization(self):
        """Test collector initialization"""
        collector = MockCollector(self.config)
        self.assertIsNotNone(collector)
        self.assertEqual(collector.service_name, 'mock')
        
    def test_create_record(self):
        """Test record creation"""
        collector = MockCollector(self.config)
        record = collector._create_record(test_field='value')
        
        self.assertIn('timestamp', record)
        self.assertIn('service', record)
        self.assertIn('test_field', record)
        self.assertEqual(record['test_field'], 'value')
        
    def test_collect(self):
        """Test data collection"""
        collector = MockCollector(self.config)
        data = collector.collect()
        
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['metric_type'], 'test')


if __name__ == '__main__':
    unittest.main()
