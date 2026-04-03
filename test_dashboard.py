#!/usr/bin/env python3
"""
Test user dashboard endpoint
"""

import requests
import json

def test_dashboard():
    """Test user dashboard loading"""
    
    base_url = "http://localhost:5002"
    
    print("Testing User Dashboard Endpoint")
    print("=" * 40)
    
    # Test endpoints
    endpoints = [
        '/api/user-dashboard',
        '/api/data',
        '/api/test-scenarios'
    ]
    
    for endpoint in endpoints:
        print(f"\nTesting: {endpoint}")
        try:
            response = requests.get(f"{base_url}{endpoint}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ SUCCESS - Status: {response.status_code}")
                
                if 'dashboard' in data:
                    users = data['dashboard'].get('users', [])
                    print(f"  Users loaded: {len(users)}")
                    print(f"  Risk summary: {data['dashboard'].get('risk_summary', {})}")
                elif 'users' in data:
                    users = data.get('users', [])
                    print(f"  Users loaded: {len(users)}")
                    print(f"  Risk summary: {data.get('risk_summary', {})}")
                elif 'scenarios' in data:
                    scenarios = data.get('scenarios', [])
                    print(f"  Scenarios loaded: {len(scenarios)}")
                else:
                    print(f"  Data keys: {list(data.keys())}")
                    
            else:
                print(f"❌ ERROR - Status: {response.status_code}")
                print(f"  Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ FAILED: {e}")

if __name__ == "__main__":
    test_dashboard()
