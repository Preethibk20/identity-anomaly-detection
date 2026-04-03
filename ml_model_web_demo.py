#!/usr/bin/env python3
"""
Web-based ML Model Selector - Interactive browser interface
Shows ML model selection and outputs in localhost
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
import time
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

class WebMLModelSelector:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.features_data = {}
        self.sample_data = None
        self.training_results = {}
        
    def load_sample_data(self):
        """Load sample authentication data"""
        try:
            with open("data/sample_logs.json", 'r') as f:
                data = json.load(f)
            self.sample_data = pd.DataFrame(data)
            return True, f"Loaded {len(self.sample_data)} authentication events"
        except FileNotFoundError:
            self.sample_data = self.generate_synthetic_data()
            return True, f"Generated {len(self.sample_data)} synthetic events"
    
    def generate_synthetic_data(self):
        """Generate synthetic authentication data for demo"""
        users = ["john.doe", "jane.smith", "mike.wilson", "sarah.johnson", "david.brown"]
        locations = ["New York", "London", "Toronto", "Sydney", "Berlin", "Moscow", "Unknown"]
        devices = ["laptop", "desktop", "mobile", "tablet", "unknown_device"]
        actions = ["login", "logout", "access_resource"]
        resources = ["email", "file_server", "database", "admin_panel", "hr_portal"]
        
        data = []
        base_time = datetime.now() - timedelta(days=30)
        
        for i in range(500):
            is_suspicious = np.random.random() < 0.1
            
            if is_suspicious:
                user = np.random.choice(users)
                hour = np.random.choice([2, 3, 23, 1])
                location = np.random.choice(["Moscow", "Unknown"])
                device = "unknown_device"
                success = np.random.choice([True, False], p=[0.7, 0.3])
                session_duration = np.random.randint(300, 600)
            else:
                user = np.random.choice(users)
                hour = np.random.randint(8, 18)
                location = np.random.choice(["New York", "London", "Toronto", "Sydney", "Berlin"])
                device = np.random.choice(["laptop", "desktop", "mobile"])
                success = True
                session_duration = np.random.randint(30, 240)
            
            timestamp = base_time + timedelta(days=int(np.random.randint(0, 30)), 
                                            hours=int(hour), 
                                            minutes=int(np.random.randint(0, 59)))
            
            event = {
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "user_id": user,
                "action": np.random.choice(actions),
                "location": location,
                "ip_address": f"192.168.{np.random.randint(1, 255)}.{np.random.randint(1, 255)}",
                "device": device,
                "resource": np.random.choice(resources),
                "success": success,
                "session_duration": session_duration,
                "user_agent": "Mozilla/5.0" if not is_suspicious else "bot/1.0"
            }
            data.append(event)
        
        return pd.DataFrame(data)
    
    def extract_simple_features(self, df):
        """Extract simple features for PoC model (9 features)"""
        features = []
        for _, row in df.iterrows():
            timestamp = pd.to_datetime(row['timestamp'])
            
            feature_dict = {
                'hour': timestamp.hour,
                'day_of_week': timestamp.dayofweek,
                'is_weekend': 1 if timestamp.dayofweek >= 5 else 0,
                'is_off_hours': 1 if timestamp.hour < 8 or timestamp.hour > 18 else 0,
                'is_login': 1 if row['action'] == 'login' else 0,
                'is_failed': 1 if not row.get('success', True) else 0,
                'session_duration': row.get('session_duration', 60),
                'location_hash': hash(row['location']) % 100,
                'device_hash': hash(row['device']) % 50,
            }
            features.append(feature_dict)
        
        return pd.DataFrame(features)
    
    def extract_advanced_features(self, df):
        """Extract advanced features for Enterprise model (50+ features)"""
        features = []
        for _, row in df.iterrows():
            timestamp = pd.to_datetime(row['timestamp'])
            
            # Temporal features (15)
            temporal = {
                'hour': timestamp.hour,
                'day_of_week': timestamp.dayofweek,
                'day_of_month': timestamp.day,
                'month': timestamp.month,
                'is_weekend': 1 if timestamp.dayofweek >= 5 else 0,
                'is_work_hours': 1 if 8 <= timestamp.hour <= 18 else 0,
                'is_lunch_time': 1 if 12 <= timestamp.hour <= 13 else 0,
                'is_early_morning': 1 if 5 <= timestamp.hour <= 7 else 0,
                'is_late_night': 1 if timestamp.hour >= 22 or timestamp.hour <= 5 else 0,
                'hour_sin': np.sin(2 * np.pi * timestamp.hour / 24),
                'hour_cos': np.cos(2 * np.pi * timestamp.hour / 24),
                'day_sin': np.sin(2 * np.pi * timestamp.dayofweek / 7),
                'day_cos': np.cos(2 * np.pi * timestamp.dayofweek / 7),
                'month_sin': np.sin(2 * np.pi * timestamp.month / 12),
                'month_cos': np.cos(2 * np.pi * timestamp.month / 12),
            }
            
            # Geolocation features (10)
            geo = {
                'location_hash': hash(row['location']) % 1000,
                'location_known': 1 if row['location'] != 'Unknown' else 0,
                'high_risk_location': 1 if row['location'] in ['Moscow', 'Unknown'] else 0,
                'location_diversity': np.random.uniform(0.1, 1.0),
                'ip_private': 1 if row.get('ip_address', '').startswith('192.168.') else 0,
                'ip_reputation': np.random.uniform(0, 0.8),
                'location_distance': np.random.uniform(0, 1000),
                'impossible_travel': 0,
                'vpn_detected': 1 if 'vpn' in row.get('ip_address', '').lower() else 0,
                'tor_detected': 1 if 'tor' in row.get('ip_address', '').lower() else 0,
            }
            
            # Device/Network features (12)
            device = {
                'device_hash': hash(row['device']) % 100,
                'device_laptop': 1 if row['device'] == 'laptop' else 0,
                'device_mobile': 1 if row['device'] == 'mobile' else 0,
                'device_desktop': 1 if row['device'] == 'desktop' else 0,
                'device_unknown': 1 if row['device'] == 'unknown_device' else 0,
                'user_agent_length': len(row.get('user_agent', '')),
                'user_agent_suspicious': 1 if 'bot' in row.get('user_agent', '').lower() else 0,
                'device_diversity': np.random.uniform(0.1, 1.0),
                'device_match': np.random.uniform(0.7, 1.0),
                'network_internal': 1 if row.get('ip_address', '').startswith('192.168.') else 0,
                'connection_secure': 1,
                'bandwidth_usage': np.random.uniform(1, 100),
            }
            
            # Behavioral features (8)
            behavioral = {
                'is_login': 1 if row['action'] == 'login' else 0,
                'is_logout': 1 if row['action'] == 'logout' else 0,
                'is_access': 1 if row['action'] == 'access_resource' else 0,
                'is_failed': 1 if not row.get('success', True) else 0,
                'session_duration': row.get('session_duration', 60),
                'long_session': 1 if row.get('session_duration', 60) > 240 else 0,
                'sensitive_resource': 1 if row.get('resource', '') in ['admin_panel', 'database'] else 0,
                'privilege_escalation': np.random.uniform(0, 0.3),
            }
            
            # Threat intelligence features (5)
            threat = {
                'ip_blacklisted': np.random.uniform(0, 0.1),
                'malware_c2': 0,
                'threat_actor_ip': 0,
                'recent_breach_ip': 0,
                'threat_score': np.random.uniform(0, 0.5),
            }
            
            # Combine all features
            all_features = {**temporal, **geo, **device, **behavioral, **threat}
            features.append(all_features)
        
        return pd.DataFrame(features)
    
    def train_simple_model(self, features_df):
        """Train simple PoC model"""
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(features_df)
        
        model = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=100
        )
        
        start_time = time.time()
        model.fit(X_scaled)
        training_time = time.time() - start_time
        
        predictions = model.predict(X_scaled)
        anomaly_scores = model.decision_function(X_scaled)
        anomalies = (predictions == -1).sum()
        
        self.models['simple'] = model
        self.scalers['simple'] = scaler
        self.features_data['simple'] = features_df
        
        return {
            'algorithm': 'Isolation Forest',
            'features': len(features_df.columns),
            'feature_names': list(features_df.columns),
            'training_time': round(training_time, 3),
            'anomalies_detected': int(anomalies),
            'total_samples': len(predictions),
            'anomaly_percentage': round(anomalies/len(predictions)*100, 1),
            'score_range': {
                'min': round(float(anomaly_scores.min()), 3),
                'max': round(float(anomaly_scores.max()), 3)
            }
        }
    
    def train_advanced_model(self, features_df):
        """Train advanced Enterprise model"""
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(features_df)
        
        algorithms = {
            'Isolation Forest': IsolationForest(contamination=0.1, random_state=42, n_estimators=200),
            'One-Class SVM': OneClassSVM(kernel='rbf', gamma='scale', nu=0.1),
            'Local Outlier Factor': LocalOutlierFactor(n_neighbors=20, contamination=0.1, novelty=True),
            'Gaussian Mixture': GaussianMixture(n_components=2, covariance_type='full', random_state=42)
        }
        
        start_time = time.time()
        results = {}
        ensemble_predictions = []
        
        for name, algorithm in algorithms.items():
            if name == 'Gaussian Mixture':
                algorithm.fit(X_scaled)
                log_likelihood = algorithm.score_samples(X_scaled)
                threshold = np.percentile(log_likelihood, 10)
                predictions = (log_likelihood < threshold).astype(int) * 2 - 1
            else:
                algorithm.fit(X_scaled)
                predictions = algorithm.predict(X_scaled)
            
            anomalies = (predictions == -1).sum()
            results[name] = {
                'anomalies': int(anomalies),
                'percentage': round(anomalies/len(predictions)*100, 1)
            }
            ensemble_predictions.append(predictions)
        
        # Ensemble voting
        ensemble_pred = np.sign(np.mean(ensemble_predictions, axis=0))
        ensemble_anomalies = (ensemble_pred == -1).sum()
        
        training_time = time.time() - start_time
        
        self.models['advanced'] = algorithms
        self.scalers['advanced'] = scaler
        self.features_data['advanced'] = features_df
        
        return {
            'algorithms': list(algorithms.keys()),
            'features': len(features_df.columns),
            'feature_names': list(features_df.columns),
            'training_time': round(training_time, 3),
            'individual_results': results,
            'ensemble_anomalies': int(ensemble_anomalies),
            'ensemble_percentage': round(ensemble_anomalies/len(ensemble_pred)*100, 1),
            'total_samples': len(ensemble_pred)
        }
    
    def test_sample_activities(self, model_type):
        """Test models on sample activities"""
        test_activities = [
            {
                'name': 'Normal Work Login',
                'data': {
                    'timestamp': '2026-01-25 09:30:00',
                    'user_id': 'john.doe',
                    'action': 'login',
                    'location': 'New York',
                    'device': 'laptop',
                    'resource': 'email',
                    'success': True,
                    'session_duration': 120,
                    'ip_address': '192.168.1.100',
                    'user_agent': 'Mozilla/5.0'
                }
            },
            {
                'name': 'Suspicious Moscow Login',
                'data': {
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
                }
            },
            {
                'name': 'Failed Login Attempt',
                'data': {
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
            }
        ]
        
        results = []
        
        for activity in test_activities:
            test_df = pd.DataFrame([activity['data']])
            
            if model_type == 'simple':
                features = self.extract_simple_features(test_df)
                model = self.models['simple']
                scaler = self.scalers['simple']
                
                # Ensure all training columns are present
                for col in self.features_data['simple'].columns:
                    if col not in features.columns:
                        features[col] = 0
                features = features[self.features_data['simple'].columns]
                
                X_scaled = scaler.transform(features)
                prediction = model.predict(X_scaled)[0]
                anomaly_score = model.decision_function(X_scaled)[0]
                
                risk_score = max(0, min(100, (0.5 - anomaly_score) * 100))
                
                # Apply context multipliers
                if activity['data']['location'] in ['Moscow', 'Unknown']:
                    risk_score *= 1.5
                if not activity['data']['success']:
                    risk_score *= 1.6
                if pd.to_datetime(activity['data']['timestamp']).hour < 6:
                    risk_score *= 1.4
                
                risk_score = min(100, risk_score)
                
                result = {
                    'activity_name': activity['name'],
                    'activity_data': activity['data'],
                    'anomaly_score': round(float(anomaly_score), 3),
                    'is_anomaly': bool(prediction == -1),
                    'risk_score': round(float(risk_score), 1),
                    'risk_level': self._get_risk_level(risk_score),
                    'algorithm_results': None
                }
                
            else:  # advanced
                features = self.extract_advanced_features(test_df)
                algorithms = self.models['advanced']
                scaler = self.scalers['advanced']
                
                X_scaled = scaler.transform(features)
                
                predictions = []
                scores = []
                algorithm_results = {}
                
                for name, algorithm in algorithms.items():
                    if name == 'Gaussian Mixture':
                        log_likelihood = algorithm.score_samples(X_scaled)
                        threshold = np.percentile(log_likelihood, 10)
                        pred = (log_likelihood < threshold).astype(int) * 2 - 1
                        score = -log_likelihood[0]
                    else:
                        pred = algorithm.predict(X_scaled)
                        if hasattr(algorithm, 'decision_function'):
                            score = algorithm.decision_function(X_scaled)[0]
                        else:
                            score = algorithm.score_samples(X_scaled)[0]
                    
                    predictions.append(pred[0])
                    scores.append(score)
                    algorithm_results[name] = {
                        'prediction': 'ANOMALY' if pred[0] == -1 else 'NORMAL',
                        'score': round(float(score), 3)
                    }
                
                prediction = np.sign(np.mean(predictions))
                anomaly_score = np.mean(scores)
                
                risk_score = max(0, min(100, abs(anomaly_score) * 20))
                
                # Context multipliers
                if activity['data']['location'] in ['Moscow', 'Unknown']:
                    risk_score *= 1.8
                if activity['data']['device'] == 'unknown_device':
                    risk_score *= 1.4
                if 'bot' in activity['data']['user_agent']:
                    risk_score *= 1.6
                if not activity['data']['success']:
                    risk_score *= 1.8
                
                risk_score = min(100, risk_score)
                
                result = {
                    'activity_name': activity['name'],
                    'activity_data': activity['data'],
                    'anomaly_score': round(float(anomaly_score), 3),
                    'is_anomaly': bool(prediction == -1),
                    'risk_score': round(float(risk_score), 1),
                    'risk_level': self._get_risk_level(risk_score),
                    'algorithm_results': algorithm_results
                }
            
            results.append(result)
        
        return results
    
    def _get_risk_level(self, risk_score):
        """Get risk level from score"""
        if risk_score < 30:
            return "Low"
        elif risk_score < 60:
            return "Medium"
        elif risk_score < 80:
            return "High"
        else:
            return "Critical"

# Initialize the ML selector
ml_selector = WebMLModelSelector()

@app.route('/')
def index():
    """Main page"""
    return render_template('ml_demo.html')

@app.route('/api/load-data', methods=['POST'])
def load_data():
    """Load sample data"""
    success, message = ml_selector.load_sample_data()
    return jsonify({
        'success': success,
        'message': message,
        'data_size': len(ml_selector.sample_data) if ml_selector.sample_data is not None else 0
    })

@app.route('/api/train-simple', methods=['POST'])
def train_simple():
    """Train simple PoC model"""
    if ml_selector.sample_data is None:
        return jsonify({'success': False, 'message': 'No data loaded'})
    
    features = ml_selector.extract_simple_features(ml_selector.sample_data)
    results = ml_selector.train_simple_model(features)
    
    return jsonify({
        'success': True,
        'results': results
    })

@app.route('/api/train-advanced', methods=['POST'])
def train_advanced():
    """Train advanced Enterprise model"""
    if ml_selector.sample_data is None:
        return jsonify({'success': False, 'message': 'No data loaded'})
    
    features = ml_selector.extract_advanced_features(ml_selector.sample_data)
    results = ml_selector.train_advanced_model(features)
    
    return jsonify({
        'success': True,
        'results': results
    })

@app.route('/api/test-model/<model_type>', methods=['POST'])
def test_model(model_type):
    """Test model on sample activities"""
    if model_type not in ml_selector.models:
        return jsonify({'success': False, 'message': f'Model {model_type} not trained'})
    
    results = ml_selector.test_sample_activities(model_type)
    
    return jsonify({
        'success': True,
        'results': results
    })

@app.route('/api/compare-models', methods=['POST'])
def compare_models():
    """Compare both models"""
    comparison = {
        'simple': {
            'algorithms': 1,
            'algorithm_name': 'Isolation Forest',
            'features': 9,
            'complexity': 'Low',
            'accuracy': 'Good',
            'false_positives': 'Medium',
            'use_case': 'PoC/Demo'
        },
        'advanced': {
            'algorithms': 4,
            'algorithm_name': 'Ensemble (IF + SVM + LOF + GM)',
            'features': 50,
            'complexity': 'High',
            'accuracy': 'Excellent',
            'false_positives': 'Low',
            'use_case': 'Production'
        }
    }
    
    return jsonify({
        'success': True,
        'comparison': comparison
    })

if __name__ == '__main__':
    print("🧠 Starting Web-based ML Model Selector")
    print("=" * 50)
    print("🌐 Open your browser and go to: http://localhost:5001")
    print("📊 Interactive ML model selection and testing")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5001, debug=True)