#!/usr/bin/env python3
"""
Enhanced Intelligence Demo - Showcasing the SECRET WEAPON features
This demonstrates what separates your project from 80% of other submissions:

1. Attack Type Classification (not just "anomaly detected")
2. User-Specific Baselines (not global models)
3. Adaptive Risk Scoring (not binary output)
4. Explainable AI (detailed reasoning)
5. Real-time Intelligence Layer
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
import time
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Import our intelligence components
from src.intelligence_layer import IntelligenceLayer
from src.user_baseline_engine import UserBaselineEngine
from src.dataset_analyzer import DatasetAnalyzer

app = Flask(__name__)
CORS(app)

class EnhancedIntelligenceDemo:
    """
    Enhanced demo showcasing the intelligence layer
    This is what makes your project UNIQUE
    """
    
    def __init__(self):
        self.intelligence = IntelligenceLayer()
        self.baseline_engine = UserBaselineEngine()
        self.dataset_analyzer = DatasetAnalyzer()
        self.ml_model = None
        self.scaler = None
        self.sample_data = None
        self.user_profiles = {}
        
        # Initialize with sample users
        self._initialize_sample_users()
    
    def _initialize_sample_users(self):
        """Initialize sample users with different roles and baselines"""
        
        # Sample historical activities for different user types
        users_data = {
            'john.doe': {
                'role': 'admin',
                'activities': self._generate_user_activities('admin', 'john.doe', 30)
            },
            'jane.smith': {
                'role': 'developer', 
                'activities': self._generate_user_activities('developer', 'jane.smith', 45)
            },
            'mike.wilson': {
                'role': 'hr',
                'activities': self._generate_user_activities('hr', 'mike.wilson', 25)
            },
            'sarah.johnson': {
                'role': 'finance',
                'activities': self._generate_user_activities('finance', 'sarah.johnson', 35)
            },
            'intern.user': {
                'role': 'intern',
                'activities': self._generate_user_activities('intern', 'intern.user', 15)
            }
        }
        
        # Create baselines for each user
        for user_id, data in users_data.items():
            baseline = self.baseline_engine.create_user_baseline(
                user_id, data['role'], data['activities']
            )
            self.user_profiles[user_id] = baseline
    
    def _generate_user_activities(self, role: str, user_id: str, count: int) -> list:
        """Generate realistic historical activities for a user role"""
        
        role_patterns = {
            'admin': {
                'hours': [8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                'locations': ['New York', 'London'],
                'devices': ['laptop', 'desktop'],
                'resources': ['admin_panel', 'database', 'email', 'file_server'],
                'session_range': (120, 480)
            },
            'developer': {
                'hours': [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                'locations': ['Berlin', 'New York', 'Toronto'],
                'devices': ['laptop'],
                'resources': ['database', 'file_server', 'email'],
                'session_range': (180, 600)
            },
            'hr': {
                'hours': [8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                'locations': ['New York'],
                'devices': ['laptop', 'desktop'],
                'resources': ['hr_portal', 'file_server', 'email'],
                'session_range': (60, 300)
            },
            'finance': {
                'hours': [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
                'locations': ['New York', 'London'],
                'devices': ['desktop'],
                'resources': ['finance_app', 'file_server', 'email'],
                'session_range': (90, 360)
            },
            'intern': {
                'hours': [9, 10, 11, 12, 13, 14, 15, 16, 17],
                'locations': ['New York'],
                'devices': ['laptop'],
                'resources': ['email', 'file_server'],
                'session_range': (30, 240)
            }
        }
        
        pattern = role_patterns.get(role, role_patterns['intern'])
        activities = []
        
        base_date = datetime.now() - timedelta(days=30)
        
        for i in range(count):
            # Generate realistic activity
            activity_date = base_date + timedelta(days=int(np.random.randint(0, 30)))
            
            # Skip some weekends for most roles
            if activity_date.weekday() >= 5 and role not in ['developer'] and np.random.random() > 0.2:
                continue
            
            hour = np.random.choice(pattern['hours'])
            activity_date = activity_date.replace(hour=int(hour), minute=int(np.random.randint(0, 59)))
            
            activity = {
                'timestamp': activity_date.strftime('%Y-%m-%d %H:%M:%S'),
                'user_id': user_id,
                'action': 'login',
                'location': np.random.choice(pattern['locations']),
                'device': np.random.choice(pattern['devices']),
                'resource': np.random.choice(pattern['resources']),
                'success': np.random.random() > 0.02,  # 2% failure rate
                'session_duration': np.random.randint(*pattern['session_range']),
                'ip_address': f"192.168.{np.random.randint(1, 255)}.{np.random.randint(1, 255)}",
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            activities.append(activity)
        
        return activities
    
    def train_ml_model(self):
        """Train a simple ML model for anomaly detection"""
        # Generate training data from all user activities
        all_activities = []
        for user_id, profile in self.user_profiles.items():
            # Get activities from baseline creation
            user_activities = self._generate_user_activities(profile['role'], user_id, 20)
            all_activities.extend(user_activities)
        
        # Add some anomalous activities
        anomalous_activities = [
            {
                'timestamp': '2026-01-25 03:00:00',
                'user_id': 'john.doe',
                'action': 'login',
                'location': 'Moscow',
                'device': 'unknown_device',
                'resource': 'admin_panel',
                'success': True,
                'session_duration': 600,
                'ip_address': '185.220.101.42',
                'user_agent': 'bot/1.0'
            },
            {
                'timestamp': '2026-01-25 23:45:00',
                'user_id': 'jane.smith',
                'action': 'login',
                'location': 'Unknown',
                'device': 'mobile',
                'resource': 'database',
                'success': False,
                'session_duration': 0,
                'ip_address': '10.0.0.1',
                'user_agent': 'curl/7.68.0'
            }
        ] * 5  # Add multiple anomalous samples
        
        all_activities.extend(anomalous_activities)
        
        # Extract features
        features = []
        for activity in all_activities:
            timestamp = pd.to_datetime(activity['timestamp'])
            
            feature_dict = {
                'hour': timestamp.hour,
                'day_of_week': timestamp.dayofweek,
                'is_weekend': 1 if timestamp.dayofweek >= 5 else 0,
                'is_off_hours': 1 if timestamp.hour < 8 or timestamp.hour > 18 else 0,
                'is_login': 1 if activity['action'] == 'login' else 0,
                'is_failed': 1 if not activity.get('success', True) else 0,
                'session_duration': activity.get('session_duration', 60),
                'location_hash': hash(activity['location']) % 100,
                'device_hash': hash(activity['device']) % 50,
            }
            features.append(feature_dict)
        
        # Train model
        features_df = pd.DataFrame(features)
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(features_df)
        
        self.ml_model = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=100
        )
        
        self.ml_model.fit(X_scaled)
        
        return {
            'success': True,
            'message': f'ML model trained on {len(all_activities)} activities',
            'features': list(features_df.columns),
            'users_trained': len(self.user_profiles)
        }
    
    def analyze_activity_with_intelligence(self, activity: dict, user_id: str) -> dict:
        """
        Analyze activity with full intelligence layer
        This is the CORE DIFFERENTIATOR
        """
        
        # Step 1: Get ML anomaly score
        if not self.ml_model or not self.scaler:
            return {'error': 'ML model not trained'}
        
        # Extract features for ML model
        timestamp = pd.to_datetime(activity['timestamp'])
        features = {
            'hour': timestamp.hour,
            'day_of_week': timestamp.dayofweek,
            'is_weekend': 1 if timestamp.dayofweek >= 5 else 0,
            'is_off_hours': 1 if timestamp.hour < 8 or timestamp.hour > 18 else 0,
            'is_login': 1 if activity['action'] == 'login' else 0,
            'is_failed': 1 if not activity.get('success', True) else 0,
            'session_duration': activity.get('session_duration', 60),
            'location_hash': hash(activity['location']) % 100,
            'device_hash': hash(activity['device']) % 50,
        }
        
        features_df = pd.DataFrame([features])
        X_scaled = self.scaler.transform(features_df)
        anomaly_score = self.ml_model.decision_function(X_scaled)[0]
        
        # Step 2: Get user baseline comparison
        if user_id in self.user_profiles:
            user_profile = self.user_profiles[user_id]
            baseline_comparison = self.baseline_engine.compare_with_baseline(user_id, activity)
        else:
            user_profile = {}
            baseline_comparison = {'error': 'No baseline found'}
        
        # Step 3: Run intelligence analysis
        intelligence_report = self.intelligence.analyze_activity(activity, anomaly_score, user_profile)
        
        # Step 4: Generate executive summary
        executive_summary = self.intelligence.generate_security_summary(intelligence_report)
        
        return {
            'intelligence_report': intelligence_report,
            'baseline_comparison': baseline_comparison,
            'executive_summary': executive_summary,
            'ml_anomaly_score': round(anomaly_score, 3),
            'user_profile_summary': {
                'role': user_profile.get('role', 'unknown'),
                'confidence': user_profile.get('confidence_score', 0),
                'primary_location': user_profile.get('primary_location', 'Unknown'),
                'primary_device': user_profile.get('primary_device', 'Unknown')
            }
        }
    
    def get_user_risk_dashboard(self) -> dict:
        """Get risk dashboard for all users"""
        dashboard_data = {
            'users': [],
            'risk_summary': {
                'total_users': len(self.user_profiles),
                'high_risk_users': 0,
                'medium_risk_users': 0,
                'low_risk_users': 0
            },
            'role_breakdown': {},
            'recent_alerts': []
        }
        
        for user_id, profile in self.user_profiles.items():
            risk_profile = self.baseline_engine.get_user_risk_profile(user_id)
            
            user_data = {
                'user_id': user_id,
                'role': profile['role'],
                'baseline_risk': profile['baseline_risk'],
                'risk_trend': profile['recent_risk_trend'],
                'confidence': profile['confidence_score'],
                'compliance': profile['role_compliance_score'],
                'last_activity': profile.get('last_activity', 'Never'),
                'risk_level': 'High' if profile['baseline_risk'] > 0.6 else 'Medium' if profile['baseline_risk'] > 0.3 else 'Low'
            }
            
            dashboard_data['users'].append(user_data)
            
            # Update counters
            if user_data['risk_level'] == 'High':
                dashboard_data['risk_summary']['high_risk_users'] += 1
            elif user_data['risk_level'] == 'Medium':
                dashboard_data['risk_summary']['medium_risk_users'] += 1
            else:
                dashboard_data['risk_summary']['low_risk_users'] += 1
            
            # Role breakdown
            role = profile['role']
            if role not in dashboard_data['role_breakdown']:
                dashboard_data['role_breakdown'][role] = {'count': 0, 'avg_risk': 0}
            dashboard_data['role_breakdown'][role]['count'] += 1
            dashboard_data['role_breakdown'][role]['avg_risk'] += profile['baseline_risk']
        
        # Calculate average risk by role
        for role_data in dashboard_data['role_breakdown'].values():
            role_data['avg_risk'] /= role_data['count']
        
        return dashboard_data

    def get_test_scenarios(self) -> list:
        """Return predefined test scenarios for the frontend"""
        scenarios = [
            {
                'name': 'Normal Admin Login',
                'description': 'Typical admin user login during work hours',
                'activity': {
                    'timestamp': '2026-01-25 10:30:00',
                    'user_id': 'john.doe',
                    'action': 'login',
                    'location': 'New York',
                    'device': 'laptop',
                    'resource': 'admin_panel',
                    'success': True,
                    'session_duration': 180,
                    'ip_address': '192.168.1.100',
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                },
                'expected_risk': 'Low'
            },
            {
                'name': 'Account Takeover Attack',
                'description': 'Suspicious login from Moscow with unknown device',
                'activity': {
                    'timestamp': '2026-01-25 03:00:00',
                    'user_id': 'john.doe',
                    'action': 'login',
                    'location': 'Moscow',
                    'device': 'unknown_device',
                    'resource': 'admin_panel',
                    'success': True,
                    'session_duration': 600,
                    'ip_address': '185.220.101.42',
                    'user_agent': 'bot/1.0'
                },
                'expected_risk': 'Critical'
            },
            {
                'name': 'Insider Threat',
                'description': 'HR user accessing finance application',
                'activity': {
                    'timestamp': '2026-01-25 14:30:00',
                    'user_id': 'mike.wilson',
                    'action': 'login',
                    'location': 'New York',
                    'device': 'laptop',
                    'resource': 'finance_app',
                    'success': True,
                    'session_duration': 300,
                    'ip_address': '192.168.1.150',
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                },
                'expected_risk': 'High'
            },
            {
                'name': 'Credential Stuffing',
                'description': 'Multiple failed login attempts with bot',
                'activity': {
                    'timestamp': '2026-01-25 23:45:00',
                    'user_id': 'jane.smith',
                    'action': 'login',
                    'location': 'Unknown',
                    'device': 'mobile',
                    'resource': 'database',
                    'success': False,
                    'session_duration': 0,
                    'ip_address': '10.0.0.1',
                    'user_agent': 'curl/7.68.0'
                },
                'expected_risk': 'High'
            },
            {
                'name': 'Developer Night Work',
                'description': 'Developer working late (normal for role)',
                'activity': {
                    'timestamp': '2026-01-25 21:00:00',
                    'user_id': 'jane.smith',
                    'action': 'login',
                    'location': 'Berlin',
                    'device': 'laptop',
                    'resource': 'database',
                    'success': True,
                    'session_duration': 480,
                    'ip_address': '192.168.2.100',
                    'user_agent': 'Mozilla/5.0 (Linux; Ubuntu)'
                },
                'expected_risk': 'Low'
            }
        ]

        return scenarios

# Initialize the enhanced demo
demo = EnhancedIntelligenceDemo()

@app.route('/')
def index():
    """Main intelligence demo page"""
    return render_template('intelligence_demo.html')

@app.route('/api/train-system', methods=['POST'])
def train_system():
    """Train the ML system and initialize baselines"""
    result = demo.train_ml_model()
    return jsonify(result)

@app.route('/api/analyze-activity', methods=['POST'])
def analyze_activity():
    """Analyze activity with full intelligence layer"""
    data = request.get_json()
    activity = data.get('activity')
    user_id = data.get('user_id')
    
    if not activity or not user_id:
        return jsonify({'error': 'Missing activity or user_id'})
    
    result = demo.analyze_activity_with_intelligence(activity, user_id)
    return jsonify(result)

@app.route('/api/data', methods=['GET'])
def get_initial_data():
    """Get initial data for frontend"""
    try:
        dashboard = demo.get_user_risk_dashboard()
        scenarios = demo.get_test_scenarios()
        return jsonify({
            'dashboard': dashboard,
            'scenarios': scenarios,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        })

@app.route('/api/user-dashboard', methods=['GET'])
def user_dashboard():
    """Get user risk dashboard"""
    dashboard = demo.get_user_risk_dashboard()
    return jsonify(dashboard)

@app.route('/api/test-scenarios', methods=['GET'])
def test_scenarios():
    """Get predefined test scenarios"""
    scenarios = [
        {
            'name': 'Normal Admin Login',
            'description': 'Typical admin user login during work hours',
            'activity': {
                'timestamp': '2026-01-25 10:30:00',
                'user_id': 'john.doe',
                'action': 'login',
                'location': 'New York',
                'device': 'laptop',
                'resource': 'admin_panel',
                'success': True,
                'session_duration': 180,
                'ip_address': '192.168.1.100',
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            },
            'expected_risk': 'Low'
        },
        {
            'name': 'Account Takeover Attack',
            'description': 'Suspicious login from Moscow with unknown device',
            'activity': {
                'timestamp': '2026-01-25 03:00:00',
                'user_id': 'john.doe',
                'action': 'login',
                'location': 'Moscow',
                'device': 'unknown_device',
                'resource': 'admin_panel',
                'success': True,
                'session_duration': 600,
                'ip_address': '185.220.101.42',
                'user_agent': 'bot/1.0'
            },
            'expected_risk': 'Critical'
        },
        {
            'name': 'Insider Threat',
            'description': 'HR user accessing finance application',
            'activity': {
                'timestamp': '2026-01-25 14:30:00',
                'user_id': 'mike.wilson',
                'action': 'login',
                'location': 'New York',
                'device': 'laptop',
                'resource': 'finance_app',
                'success': True,
                'session_duration': 300,
                'ip_address': '192.168.1.150',
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            },
            'expected_risk': 'High'
        },
        {
            'name': 'Credential Stuffing',
            'description': 'Multiple failed login attempts with bot',
            'activity': {
                'timestamp': '2026-01-25 23:45:00',
                'user_id': 'jane.smith',
                'action': 'login',
                'location': 'Unknown',
                'device': 'mobile',
                'resource': 'database',
                'success': False,
                'session_duration': 0,
                'ip_address': '10.0.0.1',
                'user_agent': 'curl/7.68.0'
            },
            'expected_risk': 'High'
        },
        {
            'name': 'Developer Night Work',
            'description': 'Developer working late (normal for role)',
            'activity': {
                'timestamp': '2026-01-25 21:00:00',
                'user_id': 'jane.smith',
                'action': 'login',
                'location': 'Berlin',
                'device': 'laptop',
                'resource': 'database',
                'success': True,
                'session_duration': 480,
                'ip_address': '192.168.2.100',
                'user_agent': 'Mozilla/5.0 (Linux; Ubuntu)'
            },
            'expected_risk': 'Low'
        }
    ]
    
    return jsonify({'scenarios': scenarios})

@app.route('/api/dataset/upload', methods=['POST'])
def upload_dataset():
    """Upload and train custom dataset"""
    try:
        data = request.get_json()
        
        if 'dataset' not in data:
            return jsonify({'error': 'No dataset provided'})
        
        # Train on the dataset
        result = demo.dataset_analyzer.train_anomaly_detector(
            pd.DataFrame(data['dataset'])
        )
        
        if 'error' in result:
            return jsonify(result)
        
        return jsonify({
            'success': True,
            'message': f'Dataset trained successfully on {result["total_records"]} records',
            'summary': {
                'total_records': result['total_records'],
                'risk_records': result['risk_records'],
                'no_risk_records': result['no_risk_records'],
                'risk_percentage': result['risk_percentage']
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Dataset upload failed: {str(e)}'})

@app.route('/api/dataset/analyze', methods=['POST'])
def analyze_new_dataset():
    """Analyze new dataset using trained model"""
    try:
        data = request.get_json()
        
        if 'dataset' not in data:
            return jsonify({'error': 'No dataset provided'})
        
        # Analyze the new dataset
        result = demo.dataset_analyzer.analyze_new_data(data['dataset'])
        
        if 'error' in result:
            return jsonify(result)
        
        return jsonify({
            'success': True,
            'summary': {
                'total_analyzed': result['total_analyzed'],
                'risk_count': result['risk_count'],
                'no_risk_count': result['no_risk_count'],
                'risk_percentage': result['risk_percentage']
            },
            'results': result['results']
        })
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'})

@app.route('/api/dataset/generate-sample', methods=['GET'])
def generate_sample_dataset():
    """Generate sample dataset for testing"""
    try:
        num_records = request.args.get('records', 1000, type=int)
        df = demo.dataset_analyzer.generate_sample_dataset(num_records)
        
        return jsonify({
            'success': True,
            'dataset': df.to_dict('records'),
            'records_count': len(df),
            'message': f'Generated {len(df)} sample records'
        })
        
    except Exception as e:
        return jsonify({'error': f'Sample generation failed: {str(e)}'})

@app.route('/api/dataset/model-info', methods=['GET'])
def get_model_info():
    """Get trained model information"""
    try:
        info = demo.dataset_analyzer.get_model_summary()
        return jsonify(info)
        
    except Exception as e:
        return jsonify({'error': f'Failed to get model info: {str(e)}'})

if __name__ == "__main__":
    print("Identity Anomaly Detection System - Starting Demo Server")
    print("=" * 60)
    print("System Features:")
    print("   • Attack Type Classification")
    print("   • User Behavioral Profiling") 
    print("   • Adaptive Risk Scoring")
    print("   • Explainable AI")
    print("   • Real-time Processing")
    print("   • Custom Dataset Analysis")
    print("=" * 60)
    print("Demo URL: http://localhost:5002")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5002, debug=True)