#!/usr/bin/env python3
"""
Simplified API Server - For demonstration without Redis dependencies
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import time
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Any
import uuid
import os
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'demo-secret-key'
CORS(app, origins=["*"])

# Global system metrics
system_metrics = {
    'start_time': time.time(),
    'events_processed': 1245,
    'alerts_generated': 23,
    'api_requests': 0,
}

# Mock data storage
mock_alerts = [
    {
        'id': 'alert-001',
        'title': 'Suspicious Login from Moscow',
        'description': 'User john.doe logged in from unusual location at 3 AM',
        'severity': 'high',
        'status': 'open',
        'timestamp': (datetime.now() - timedelta(hours=2)).isoformat(),
        'user_id': 'john.doe',
        'risk_score': 85,
    },
    {
        'id': 'alert-002',
        'title': 'Multiple Failed Login Attempts',
        'description': 'User jane.smith had 5 failed login attempts in 2 minutes',
        'severity': 'medium',
        'status': 'investigating',
        'timestamp': (datetime.now() - timedelta(hours=1)).isoformat(),
        'user_id': 'jane.smith',
        'risk_score': 65,
    },
    {
        'id': 'alert-003',
        'title': 'Impossible Travel Detected',
        'description': 'User mike.wilson appeared in Tokyo 30 minutes after New York login',
        'severity': 'critical',
        'status': 'open',
        'timestamp': (datetime.now() - timedelta(minutes=30)).isoformat(),
        'user_id': 'mike.wilson',
        'risk_score': 95,
    },
]

@app.before_request
def before_request():
    """Track API requests"""
    system_metrics['api_requests'] += 1

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'uptime': time.time() - system_metrics['start_time'],
        'version': '1.0.0',
        'message': 'Enterprise Identity Anomaly Detection System is running'
    })

@app.route('/api/dashboard/metrics', methods=['GET'])
def get_dashboard_metrics():
    """Get dashboard metrics"""
    uptime = time.time() - system_metrics['start_time']
    
    return jsonify({
        'totalUsers': 156,
        'activeAlerts': len([a for a in mock_alerts if a['status'] == 'open']),
        'highRiskAlerts': len([a for a in mock_alerts if a['severity'] in ['high', 'critical']]),
        'criticalAlerts': len([a for a in mock_alerts if a['severity'] == 'critical']),
        'eventsProcessed': system_metrics['events_processed'],
        'eventsPerSecond': round(system_metrics['events_processed'] / uptime if uptime > 0 else 0, 1),
        'avgProcessingTime': 85.2,
        'systemUptime': uptime,
        'threatScore': 65,
        'falsePositiveRate': 2.1,
    })

@app.route('/api/alerts/recent', methods=['GET'])
def get_recent_alerts():
    """Get recent alerts"""
    limit = request.args.get('limit', 10, type=int)
    return jsonify(mock_alerts[:limit])

@app.route('/api/analytics/risk-trends', methods=['GET'])
def get_risk_trends():
    """Get risk trends data"""
    time_range = request.args.get('range', '24h')
    
    # Generate sample trend data
    now = datetime.now()
    data = []
    
    if time_range == '1h':
        points, interval = 12, 5
    elif time_range == '6h':
        points, interval = 24, 15
    elif time_range == '24h':
        points, interval = 48, 30
    else:  # 7d
        points, interval = 168, 60
    
    for i in range(points, -1, -1):
        timestamp = now - timedelta(minutes=i * interval)
        base_risk = 30 + (i % 20) + (i % 7) * 5
        
        data.append({
            'timestamp': timestamp.isoformat(),
            'avgRiskScore': max(0, min(100, base_risk)),
            'alertCount': max(1, (i % 10) + 1),
            'criticalAlerts': max(0, (i % 5) - 2),
            'highAlerts': max(1, (i % 7)),
            'mediumAlerts': max(2, (i % 8) + 2),
            'lowAlerts': max(3, (i % 12) + 3),
        })
    
    return jsonify(data)

@app.route('/api/analytics/location-activity', methods=['GET'])
def get_location_activity():
    """Get location activity data"""
    locations = [
        {
            'location': 'New York',
            'userCount': 45,
            'activityCount': 1250,
            'riskScore': 25,
            'coordinates': [40.7128, -74.0060],
            'topUsers': ['john.doe', 'jane.smith', 'mike.wilson'],
            'alertCount': 2,
        },
        {
            'location': 'London',
            'userCount': 32,
            'activityCount': 890,
            'riskScore': 35,
            'coordinates': [51.5074, -0.1278],
            'topUsers': ['alice.brown', 'bob.jones'],
            'alertCount': 4,
        },
        {
            'location': 'Moscow',
            'userCount': 3,
            'activityCount': 45,
            'riskScore': 85,
            'coordinates': [55.7558, 37.6176],
            'topUsers': ['unknown.user'],
            'alertCount': 8,
        },
    ]
    
    return jsonify(locations)

@app.route('/api/threat-intel', methods=['GET'])
def get_threat_intelligence():
    """Get threat intelligence data"""
    threat_data = {
        'ipThreats': [
            {
                'ip': '185.220.101.42',
                'threatType': 'Tor Exit Node',
                'severity': 'high',
                'lastSeen': '2026-01-25T15:30:00Z',
                'description': 'Known Tor exit node used for anonymization',
            },
            {
                'ip': '45.142.214.123',
                'threatType': 'Botnet C2',
                'severity': 'critical',
                'lastSeen': '2026-01-25T14:45:00Z',
                'description': 'Command and control server for Emotet botnet',
            },
        ],
        'malwareDomains': [
            {
                'domain': 'malicious-site.com',
                'malwareFamily': 'TrickBot',
                'firstSeen': '2026-01-24T10:00:00Z',
                'confidence': 95,
            },
        ],
        'threatActors': [
            {
                'name': 'APT29 (Cozy Bear)',
                'techniques': ['Spear Phishing', 'Credential Dumping', 'Lateral Movement'],
                'lastActivity': '2026-01-20T00:00:00Z',
                'targetSectors': ['Government', 'Healthcare', 'Technology'],
            },
        ],
        'vulnerabilities': [
            {
                'cve': 'CVE-2024-1234',
                'severity': 'Critical',
                'description': 'Remote code execution in authentication service',
                'exploitAvailable': True,
            },
        ],
    }
    
    return jsonify(threat_data)

@app.route('/api/system/simulate-attack', methods=['POST'])
def simulate_attack():
    """Simulate a security attack for testing"""
    try:
        # Create a new alert
        new_alert = {
            'id': f'alert-{len(mock_alerts) + 1:03d}',
            'title': 'SIMULATED: Suspicious Login from Unknown Location',
            'description': 'Simulated attack: User attempted login from suspicious IP address',
            'severity': 'critical',
            'status': 'open',
            'timestamp': datetime.now().isoformat(),
            'user_id': 'test.user',
            'risk_score': 92,
        }
        
        mock_alerts.insert(0, new_alert)
        system_metrics['alerts_generated'] += 1
        system_metrics['events_processed'] += 1
        
        return jsonify({
            'success': True,
            'message': 'Attack simulation completed successfully',
            'alert': new_alert
        })
        
    except Exception as e:
        logger.error(f"Attack simulation failed: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/system/health', methods=['GET'])
def get_system_health():
    """Get system health metrics"""
    uptime = time.time() - system_metrics['start_time']
    
    return jsonify({
        'status': 'healthy',
        'uptime': uptime,
        'components': {
            'api_server': 'healthy',
            'ml_engine': 'healthy',
            'alert_manager': 'healthy',
            'database': 'healthy',
        },
        'metrics': {
            'events_processed': system_metrics['events_processed'],
            'alerts_generated': system_metrics['alerts_generated'],
            'api_requests': system_metrics['api_requests'],
            'memory_usage': 65.2,
            'cpu_usage': 45.8,
        }
    })

@app.route('/api/analytics/users', methods=['GET'])
def get_user_analytics():
    """Get user analytics data"""
    users_data = [
        {
            'id': 'john.doe',
            'name': 'John Doe',
            'email': 'john.doe@company.com',
            'department': 'Engineering',
            'riskScore': 85,
            'lastActivity': '2026-01-25T16:30:00Z',
            'totalActivities': 1250,
            'alertCount': 8,
            'status': 'High Risk',
        },
        {
            'id': 'jane.smith',
            'name': 'Jane Smith',
            'email': 'jane.smith@company.com',
            'department': 'Marketing',
            'riskScore': 25,
            'lastActivity': '2026-01-25T15:45:00Z',
            'totalActivities': 890,
            'alertCount': 2,
            'status': 'Normal',
        },
    ]
    
    return jsonify(users_data)

@app.route('/api/threat-hunting/search', methods=['POST'])
def search_threats():
    """Search for threats based on query"""
    data = request.get_json()
    query = data.get('query', '')
    
    # Mock search results
    results = [
        {
            'id': 'result-1',
            'type': 'User Activity',
            'title': 'Suspicious login pattern for john.doe',
            'description': 'Multiple logins from different countries within 1 hour',
            'timestamp': '2026-01-25T15:30:00Z',
            'riskScore': 85,
            'entities': ['john.doe', '185.220.101.42', 'Moscow'],
        },
        {
            'id': 'result-2',
            'type': 'Network Activity',
            'title': 'Unusual data transfer volume',
            'description': 'Large file downloads during off-hours',
            'timestamp': '2026-01-25T14:45:00Z',
            'riskScore': 65,
            'entities': ['jane.smith', '192.168.1.100', 'file-server'],
        },
    ]
    
    return jsonify(results)

@app.route('/api/reports', methods=['GET'])
def get_reports():
    """Get available reports"""
    reports = [
        {
            'id': 'report-001',
            'name': 'Weekly Security Summary',
            'type': 'Security Summary',
            'status': 'Completed',
            'createdAt': '2026-01-25T10:00:00Z',
            'size': '2.3 MB',
            'format': 'PDF',
            'description': 'Comprehensive weekly security overview with key metrics and trends',
        },
        {
            'id': 'report-002',
            'name': 'User Risk Assessment',
            'type': 'Risk Assessment',
            'status': 'Completed',
            'createdAt': '2026-01-24T15:30:00Z',
            'size': '1.8 MB',
            'format': 'Excel',
            'description': 'Detailed analysis of user risk scores and behavioral patterns',
        },
    ]
    
    return jsonify(reports)

# Authentication endpoints (mock)
@app.route('/api/auth/login', methods=['POST'])
def login():
    """Mock login endpoint"""
    data = request.get_json()
    username = data.get('username', 'demo')
    
    return jsonify({
        'success': True,
        'token': 'demo-jwt-token-12345',
        'user': {
            'id': 'user-123',
            'username': username,
            'email': f'{username}@company.com',
            'role': 'Security Analyst',
            'permissions': ['view_alerts', 'manage_alerts', 'view_analytics'],
        }
    })

@app.route('/api/auth/verify', methods=['GET'])
def verify_token():
    """Mock token verification"""
    return jsonify({'valid': True})

def update_metrics():
    """Update system metrics periodically"""
    while True:
        time.sleep(5)
        system_metrics['events_processed'] += 5
        if len(mock_alerts) > 0:
            # Simulate some alerts being resolved
            for alert in mock_alerts:
                if alert['status'] == 'open' and time.time() % 30 < 5:
                    alert['status'] = 'investigating'

if __name__ == '__main__':
    print("🚀 Starting Enterprise Identity Anomaly Detection API Server")
    print("=" * 60)
    print("✅ System initialized successfully")
    print("🌐 API Server: http://localhost:8000")
    print("📊 Health Check: http://localhost:8000/api/health")
    print("📋 Dashboard Metrics: http://localhost:8000/api/dashboard/metrics")
    print("=" * 60)
    
    # Start background metrics updater
    metrics_thread = threading.Thread(target=update_metrics, daemon=True)
    metrics_thread.start()
    
    # Run the server
    app.run(host='0.0.0.0', port=8000, debug=True)