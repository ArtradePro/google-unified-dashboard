#!/usr/bin/env python3
"""
Demo script to test the dashboard with sample data (no API keys required)
"""

import os
import sys
from datetime import datetime, timezone

# Temporarily disable credential requirements for demo
os.environ['DEMO_MODE'] = '1'

from src.utils.aggregator import DataAggregator
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def create_sample_data():
    """Create sample data for demonstration"""
    
    sample_data = [
        # Gemini sample data
        {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'service': 'gemini',
            'metric_type': 'api_usage',
            'input_token': 150000,
            'output_token': 50000,
            'api_calls': 250,
            'models': 'gemini-pro, gemini-pro-vision'
        },
        # Opal sample data
        {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'service': 'opal',
            'metric_type': 'platform_usage',
            'api_call': 1250,
            'active_users': 45,
            'user_seat': 50,
            'resources_managed': 320
        },
        # Wisk sample data
        {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'service': 'wisk',
            'metric_type': 'platform_usage',
            'api_call': 850,
            'storage_gb': 125.5,
            'data_transfers_gb': 45.2,
            'active_projects': 12
        },
        # Polemi sample data
        {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'service': 'polemi',
            'metric_type': 'compute_usage',
            'api_call': 650,
            'compute_hour': 85.5,
            'memory_gb_hours': 340,
            'active_jobs': 28
        }
    ]
    
    return sample_data


def main():
    """Run the demo"""
    
    print("=" * 60)
    print("Google Unified Dashboard - DEMO MODE")
    print("=" * 60)
    print()
    
    # Sample configuration
    config = {
        'cost_mapping': {
            'gemini': {
                'input_token': 0.000001,
                'output_token': 0.000002
            },
            'opal': {
                'api_call': 0.01,
                'user_seat': 50.00
            },
            'wisk': {
                'api_call': 0.005,
                'storage_gb': 0.10
            },
            'polemi': {
                'api_call': 0.008,
                'compute_hour': 0.50
            }
        }
    }
    
    # Create aggregator
    aggregator = DataAggregator(config)
    
    # Generate sample data
    print("1. Generating sample usage data...")
    sample_data = create_sample_data()
    print(f"   Created {len(sample_data)} sample records")
    print()
    
    # Aggregate data
    print("2. Aggregating and calculating costs...")
    aggregated_data = aggregator.aggregate(sample_data)
    print(f"   Aggregated {len(aggregated_data)} records")
    print()
    
    # Display results
    print("3. Results:")
    print("-" * 60)
    
    total_cost = 0.0
    for record in aggregated_data:
        service = record['service']
        cost = record['calculated_cost']
        total_cost += cost
        
        print(f"\n   Service: {service.upper()}")
        print(f"   Metric Type: {record.get('metric_type', 'N/A')}")
        
        # Display relevant metrics for each service
        if service == 'gemini':
            print(f"   Input Tokens: {record.get('input_token', 0):,}")
            print(f"   Output Tokens: {record.get('output_token', 0):,}")
            print(f"   API Calls: {record.get('api_calls', 0):,}")
        elif service == 'opal':
            print(f"   API Calls: {record.get('api_call', 0):,}")
            print(f"   Active Users: {record.get('active_users', 0)}")
            print(f"   User Seats: {record.get('user_seat', 0)}")
        elif service == 'wisk':
            print(f"   API Calls: {record.get('api_call', 0):,}")
            print(f"   Storage: {record.get('storage_gb', 0):.1f} GB")
            print(f"   Active Projects: {record.get('active_projects', 0)}")
        elif service == 'polemi':
            print(f"   API Calls: {record.get('api_call', 0):,}")
            print(f"   Compute Hours: {record.get('compute_hour', 0):.1f}")
            print(f"   Active Jobs: {record.get('active_jobs', 0)}")
            
        print(f"   Calculated Cost: ${cost:.4f}")
    
    print("\n" + "-" * 60)
    print(f"\n   TOTAL COST: ${total_cost:.4f}")
    print()
    
    print("=" * 60)
    print("Demo completed successfully!")
    print()
    print("Next steps:")
    print("1. Configure API keys in .env file")
    print("2. Set up Google Sheets credentials (service-account.json)")
    print("3. Run: python main.py")
    print("4. View data in Google Sheets")
    print("5. Connect Looker Studio to visualize")
    print("=" * 60)


if __name__ == "__main__":
    main()
