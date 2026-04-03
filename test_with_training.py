#!/usr/bin/env python3
"""
Test scenarios with proper system training
"""

import requests
import json

def test_with_training():
    """Test scenarios with system training"""
    
    base_url = "http://localhost:5002"
    
    print("Testing Scenarios with System Training")
    print("=" * 50)
    
    # Step 1: Train the system
    print("\n1. Training system...")
    try:
        response = requests.post(f"{base_url}/api/train-system")
        training_result = response.json()
        print(f"   Training: {training_result.get('message', 'Failed')}")
    except Exception as e:
        print(f"   Training failed: {e}")
        return
    
    # Step 2: Get scenarios
    print("\n2. Loading scenarios...")
    try:
        response = requests.get(f"{base_url}/api/test-scenarios")
        scenarios = response.json()['scenarios']
        print(f"   Loaded {len(scenarios)} scenarios")
    except Exception as e:
        print(f"   Failed to load scenarios: {e}")
        return
    
    # Step 3: Test each scenario
    print("\n3. Testing scenarios...")
    for i, scenario in enumerate(scenarios):
        print(f"\n{i+1}. Scenario: {scenario['name']}")
        print(f"   Expected: {scenario['expected_risk']} Risk")
        
        try:
            response = requests.post(
                f"{base_url}/api/analyze-activity",
                json={
                    "activity": scenario['activity'],
                    "user_id": scenario['activity']['user_id']
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                report = result.get('intelligence_report', {})
                
                actual_score = report.get('risk_score', 0)
                actual_level = report.get('risk_level', 'Unknown')
                attack_type = report.get('attack_type', 'Unknown')
                
                print(f"   Actual: {actual_level} Risk ({actual_score}/100)")
                print(f"   Attack: {attack_type}")
                
                # Verify it's working correctly
                if actual_score > 0:
                    print("   ✅ Analysis successful")
                else:
                    print("   ⚠️  Zero risk score - check analysis")
                    
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Scenario testing complete!")
    print("\nTo test in browser:")
    print("1. Go to http://localhost:5002")
    print("2. Click 'Initialize System'")
    print("3. Click 'Load Test Scenarios'")
    print("4. Click any scenario card")
    print("5. Check the results banner shows correct scenario name")

if __name__ == "__main__":
    test_with_training()
