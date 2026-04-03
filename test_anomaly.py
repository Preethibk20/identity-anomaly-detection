#!/usr/bin/env python3
"""
Test script to check anomaly detection and risk scoring
"""

import requests
import json

def test_anomaly_detection():
    """Test with known anomalous activities"""
    
    base_url = "http://localhost:5002"
    
    # Test cases that should be HIGH RISK
    test_cases = [
        {
            "name": "Account Takeover Attack",
            "user_id": "john.doe",
            "activity": {
                "timestamp": "2026-01-25 03:00:00",
                "user_id": "john.doe",
                "action": "login",
                "location": "Moscow",
                "device": "unknown_device",
                "resource": "admin_panel",
                "success": True,
                "session_duration": 600,
                "ip_address": "185.220.101.42",
                "user_agent": "bot/1.0"
            },
            "expected_risk": "High"
        },
        {
            "name": "Insider Threat",
            "user_id": "mike.wilson", 
            "activity": {
                "timestamp": "2026-01-25 14:30:00",
                "user_id": "mike.wilson",
                "action": "login",
                "location": "New York",
                "device": "laptop",
                "resource": "finance_app",
                "success": True,
                "session_duration": 300,
                "ip_address": "192.168.1.150",
                "user_agent": "Mozilla/5.0"
            },
            "expected_risk": "High"
        },
        {
            "name": "Credential Stuffing",
            "user_id": "jane.smith",
            "activity": {
                "timestamp": "2026-01-25 23:45:00", 
                "user_id": "jane.smith",
                "action": "login",
                "location": "Unknown",
                "device": "mobile",
                "resource": "database",
                "success": False,
                "session_duration": 0,
                "ip_address": "10.0.0.1",
                "user_agent": "curl/7.68.0"
            },
            "expected_risk": "High"
        }
    ]
    
    print("Testing Anomaly Detection System")
    print("=" * 50)
    
    # First train the system
    try:
        response = requests.post(f"{base_url}/api/train-system")
        print(f"Training system: {response.json()}")
    except Exception as e:
        print(f"Training failed: {e}")
        return
    
    # Test each case
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['name']}")
        print(f"Expected Risk: {test_case['expected_risk']}")
        
        try:
            response = requests.post(
                f"{base_url}/api/analyze-activity",
                json={
                    "user_id": test_case["user_id"],
                    "activity": test_case["activity"]
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                risk_score = result.get('intelligence_report', {}).get('risk_score', 0)
                risk_level = result.get('intelligence_report', {}).get('risk_level', 'Unknown')
                anomaly_score = result.get('intelligence_report', {}).get('anomaly_score', 0)
                attack_type = result.get('intelligence_report', {}).get('attack_type', 'Unknown')
                
                print(f"Actual Risk Score: {risk_score}")
                print(f"Actual Risk Level: {risk_level}")
                print(f"Anomaly Score: {anomaly_score}")
                print(f"Attack Type: {attack_type}")
                
                # Check if detection is working
                if risk_score < 50 and test_case['expected_risk'] == 'High':
                    print("❌ PROBLEM: Low risk score for high-risk scenario!")
                elif risk_score >= 50:
                    print("✅ Good: High risk score detected")
                else:
                    print("⚠️  Medium risk detected")
                    
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_anomaly_detection()
