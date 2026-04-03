#!/usr/bin/env python3
"""
Test the new dataset analysis feature
"""

import requests
import json

def test_dataset_analysis():
    """Test the dataset analysis functionality"""
    
    base_url = "http://localhost:5002"
    
    print("🚀 Testing Dataset Analysis Feature")
    print("=" * 60)
    
    # Step 1: Generate sample dataset
    print("\n1. Generating sample dataset...")
    try:
        response = requests.get(f"{base_url}/api/dataset/generate-sample?records=500")
        data = response.json()
        
        if data['success']:
            sample_data = data['dataset']
            print(f"   ✅ Generated {data['records_count']} sample records")
            print(f"   Sample record: {sample_data[0]}")
        else:
            print(f"   ❌ Failed: {data['error']}")
            return
            
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return
    
    # Step 2: Train model on sample dataset
    print("\n2. Training model on dataset...")
    try:
        response = requests.post(f"{base_url}/api/dataset/upload", json={
            'dataset': sample_data
        })
        
        result = response.json()
        
        if result['success']:
            print(f"   ✅ Training successful!")
            print(f"   Total records: {result['summary']['total_records']}")
            print(f"   Risk records: {result['summary']['risk_records']}")
            print(f"   No-risk records: {result['summary']['no_risk_records']}")
            print(f"   Risk percentage: {result['summary']['risk_percentage']}%")
        else:
            print(f"   ❌ Training failed: {result['error']}")
            return
            
    except Exception as e:
        print(f"   ❌ Training failed: {e}")
        return
    
    # Step 3: Analyze new data
    print("\n3. Analyzing new test data...")
    
    # Create some test data with known patterns
    test_data = [
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
        },
        {
            'user_id': 'bob',
            'timestamp': '2026-01-25 23:45:00',
            'action': 'login',
            'location': 'Moscow',
            'device': 'unknown_device',
            'resource': 'admin_panel',
            'session_duration': 300,
            'success': True,
            'ip_address': '10.0.0.1',
            'user_agent': 'bot/1.0'
        },
        {
            'user_id': 'charlie',
            'timestamp': '2026-01-25 09:15:00',
            'action': 'access_resource',
            'location': 'London',
            'device': 'desktop',
            'resource': 'database',
            'session_duration': 45,
            'success': True,
            'ip_address': '192.168.2.50',
            'user_agent': 'Mozilla/5.0'
        }
    ]
    
    try:
        response = requests.post(f"{base_url}/api/dataset/analyze", json={
            'dataset': test_data
        })
        
        result = response.json()
        
        if result['success']:
            print(f"   ✅ Analysis successful!")
            print(f"   Total analyzed: {result['summary']['total_analyzed']}")
            print(f"   Risk records: {result['summary']['risk_count']}")
            print(f"   No-risk records: {result['summary']['no_risk_count']}")
            print(f"   Risk percentage: {result['summary']['risk_percentage']}%")
            
            print("\n   Detailed Results:")
            for i, analysis in enumerate(result['results']):
                print(f"   Record {i+1}:")
                print(f"     User: {analysis['original_data']['user_id']}")
                print(f"     Location: {analysis['original_data']['location']}")
                print(f"     Device: {analysis['original_data']['device']}")
                print(f"     Category: {analysis['risk_category']}")
                print(f"     Anomaly Score: {analysis['anomaly_score']}")
                print(f"     Confidence: {analysis['confidence']:.2f}")
                print()
                
        else:
            print(f"   ❌ Analysis failed: {result['error']}")
            return
            
    except Exception as e:
        print(f"   ❌ Analysis failed: {e}")
        return
    
    # Step 4: Get model info
    print("\n4. Getting model information...")
    try:
        response = requests.get(f"{base_url}/api/dataset/model-info")
        info = response.json()
        
        if 'error' not in info:
            print(f"   ✅ Model Info:")
            print(f"   Model type: {info['model_type']}")
            print(f"   Feature columns: {info['feature_columns']}")
            print(f"   Label encoders: {info['label_encoders']}")
            print(f"   Is trained: {info['is_trained']}")
        else:
            print(f"   ❌ Failed: {info['error']}")
            
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Dataset Analysis Feature Test Complete!")
    print("\n📋 How to use the feature:")
    print("1. Go to http://localhost:5002")
    print("2. Click 'Dataset Analyzer' button")
    print("3. Generate sample data or upload your own dataset")
    print("4. Train the model on your dataset")
    print("5. Analyze new data to categorize as Risk/No-Risk")
    print("\n📊 The system will automatically categorize activities as:")
    print("   • Risk: Suspicious/anomalous activities")
    print("   • No-Risk: Normal/legitimate activities")

if __name__ == "__main__":
    test_dataset_analysis()
