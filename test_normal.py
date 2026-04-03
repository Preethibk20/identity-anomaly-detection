#!/usr/bin/env python3
"""
Test normal admin login specifically
"""

import requests
import json

def test_normal_admin():
    """Test normal admin login scenario"""
    
    base_url = "http://localhost:5002"
    
    # Normal admin login data
    normal_activity = {
        "user_id": "john.doe",
        "activity": {
            "timestamp": "2026-01-25 10:30:00",
            "user_id": "john.doe",
            "action": "login",
            "location": "New York",
            "device": "laptop",
            "resource": "admin_panel",
            "success": True,
            "session_duration": 180,
            "ip_address": "192.168.1.100",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
    }
    
    print("Testing Normal Admin Login")
    print("=" * 40)
    
    # Train system first
    try:
        response = requests.post(f"{base_url}/api/train-system")
        print(f"Training: {response.json()}")
    except Exception as e:
        print(f"Training failed: {e}")
        return
    
    # Test normal activity
    try:
        response = requests.post(
            f"{base_url}/api/analyze-activity",
            json=normal_activity
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("\nResults:")
            print(f"Risk Score: {result.get('intelligence_report', {}).get('risk_score', 0)}")
            print(f"Risk Level: {result.get('intelligence_report', {}).get('risk_level', 'Unknown')}")
            print(f"Anomaly Score: {result.get('intelligence_report', {}).get('anomaly_score', 0)}")
            print(f"Attack Type: {result.get('intelligence_report', {}).get('attack_type', 'Unknown')}")
            
            # Check components
            risk_analysis = result.get('intelligence_report', {}).get('risk_analysis', {})
            components = risk_analysis.get('components', {})
            
            print(f"\nRisk Components:")
            for component, value in components.items():
                print(f"  {component}: {value}")
                
            # Expected vs Actual
            expected_level = "Low"
            actual_level = result.get('intelligence_report', {}).get('risk_level', 'Unknown')
            actual_score = result.get('intelligence_report', {}).get('risk_score', 0)
            
            print(f"\nExpected: {expected_level} (score < 30)")
            print(f"Actual: {actual_level} (score {actual_score})")
            
            if actual_score < 30:
                print("✅ CORRECT: Low risk detected")
            elif actual_score < 60:
                print("❌ PROBLEM: Medium risk for normal activity")
            else:
                print("❌ PROBLEM: High risk for normal activity")
                
        else:
            print(f"Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_normal_admin()
