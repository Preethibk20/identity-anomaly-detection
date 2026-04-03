#!/usr/bin/env python3
"""
Debug dataset analyzer directly
"""

import sys
sys.path.append('.')

from src.dataset_analyzer import DatasetAnalyzer
import pandas as pd

def debug_analyzer():
    """Debug the dataset analyzer"""
    
    print("🔍 Debugging Dataset Analyzer")
    print("=" * 40)
    
    # Create analyzer
    analyzer = DatasetAnalyzer()
    
    # Generate sample data
    print("\n1. Generating sample data...")
    df = analyzer.generate_sample_dataset(100)
    print(f"   Generated {len(df)} records")
    print(f"   Columns: {list(df.columns)}")
    
    # Train model
    print("\n2. Training model...")
    result = analyzer.train_anomaly_detector(df)
    print(f"   Result keys: {list(result.keys())}")
    
    if 'error' in result:
        print(f"   ❌ Error: {result['error']}")
    else:
        print(f"   ✅ Success!")
        print(f"   Total records: {result.get('total_records', 'N/A')}")
        print(f"   Risk records: {result.get('risk_records', 'N/A')}")
        print(f"   No-risk records: {result.get('no_risk_records', 'N/A')}")
        print(f"   Risk percentage: {result.get('risk_percentage', 'N/A')}")
    
    # Test with new data
    print("\n3. Testing with new data...")
    new_data = [
        {
            'user_id': 'alice',
            'timestamp': '2026-01-25 14:30:00',
            'action': 'login',
            'location': 'New York',
            'device': 'laptop',
            'resource': 'email',
            'session_duration': 120,
            'success': True,
            'ip_address': '192.168.1.100',
            'user_agent': 'Mozilla/5.0'
        }
    ]
    
    result2 = analyzer.analyze_new_data(new_data)
    print(f"   Result keys: {list(result2.keys())}")
    
    if 'error' in result2:
        print(f"   ❌ Error: {result2['error']}")
    else:
        print(f"   ✅ Analysis successful!")
        print(f"   Total analyzed: {result2.get('total_analyzed', 'N/A')}")
        print(f"   Risk count: {result2.get('risk_count', 'N/A')}")
        print(f"   No-risk count: {result2.get('no_risk_count', 'N/A')}")

if __name__ == "__main__":
    debug_analyzer()
