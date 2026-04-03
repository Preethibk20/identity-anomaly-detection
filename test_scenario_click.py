#!/usr/bin/env python3
"""
Test different scenarios to verify clicking works correctly
"""

import requests
import json

def test_all_scenarios():
    """Test all scenarios to verify correct data display"""
    
    base_url = "http://localhost:5002"
    
    # Get scenarios first
    try:
        response = requests.get(f"{base_url}/api/test-scenarios")
        scenarios = response.json()['scenarios']
    except:
        print("Failed to load scenarios")
        return
    
    print("Testing All Scenarios")
    print("=" * 50)
    
    for i, scenario in enumerate(scenarios):
        print(f"\n{i+1}. Testing: {scenario['name']}")
        print(f"   Expected: {scenario['expected_risk']} Risk")
        
        try:
            # Analyze each scenario
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
                
                # Check if it matches expectation
                if scenario['expected_risk'].lower() in ['low', 'medium'] and actual_level.lower() in ['low', 'medium']:
                    print("   ✅ Risk level appropriate")
                elif scenario['expected_risk'].lower() in ['high', 'critical'] and actual_level.lower() in ['high', 'critical']:
                    print("   ✅ Risk level appropriate")
                else:
                    print("   ⚠️  Risk level may not match expectation")
                    
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Failed: {e}")

if __name__ == "__main__":
    test_all_scenarios()
