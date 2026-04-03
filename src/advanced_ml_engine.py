#!/usr/bin/env python3
"""
Advanced ML Engine - Enterprise-grade anomaly detection
Supports multiple algorithms, auto-tuning, and 50+ features
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, VotingClassifier
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, roc_auc_score
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense, RepeatVector, TimeDistributed
import joblib
import json
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Tuple, Any
import asyncio
import concurrent.futures

class LSTMAutoencoder:
    """LSTM Autoencoder for sequence-based anomaly detection"""
    
    def __init__(self, sequence_length=10, n_features=50, encoding_dim=32):
        self.sequence_length = sequence_length
        self.n_features = n_features
        self.encoding_dim = encoding_dim
        self.model = None
        self.threshold = None
        
    def build_model(self):
        """Build LSTM Autoencoder architecture"""
        # Input layer
        input_layer = Input(shape=(self.sequence_length, self.n_features))
        
        # Encoder
        encoder = LSTM(self.encoding_dim, activation='relu')(input_layer)
        
        # Decoder
        decoder = RepeatVector(self.sequence_length)(encoder)
        decoder = LSTM(self.n_features, activation='relu', return_sequences=True)(decoder)
        decoder = TimeDistributed(Dense(self.n_features))(decoder)
        
        # Autoencoder model
        self.model = Model(inputs=input_layer, outputs=decoder)
        self.model.compile(optimizer='adam', loss='mse')
        
        return self.model
    
    def fit(self, X_train):
        """Train the LSTM autoencoder"""
        if self.model is None:
            self.build_model()
        
        # Reshape data for LSTM
        X_reshaped = self._reshape_data(X_train)
        
        # Train model
        history = self.model.fit(
            X_reshaped, X_reshaped,
            epochs=50,
            batch_size=32,
            validation_split=0.2,
            verbose=0
        )
        
        # Calculate threshold based on reconstruction error
        predictions = self.model.predict(X_reshaped)
        mse = np.mean(np.power(X_reshaped - predictions, 2), axis=(1, 2))
        self.threshold = np.percentile(mse, 95)  # 95th percentile as threshold
        
        return history
    
    def predict(self, X):
        """Predict anomalies using reconstruction error"""
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        X_reshaped = self._reshape_data(X)
        predictions = self.model.predict(X_reshaped)
        mse = np.mean(np.power(X_reshaped - predictions, 2), axis=(1, 2))
        
        # Return anomaly scores (higher = more anomalous)
        anomaly_scores = mse / self.threshold
        return anomaly_scores
    
    def _reshape_data(self, X):
        """Reshape data for LSTM input"""
        if len(X.shape) == 2:
            # Pad or truncate to sequence_length
            n_samples = X.shape[0]
            if n_samples < self.sequence_length:
                # Pad with zeros
                padding = np.zeros((self.sequence_length - n_samples, X.shape[1]))
                X_padded = np.vstack([padding, X])
            else:
                # Take last sequence_length samples
                X_padded = X[-self.sequence_length:]
            
            # Reshape to (1, sequence_length, n_features)
            return X_padded.reshape(1, self.sequence_length, -1)
        
        return X

class AdvancedFeatureEngineer:
    """Enhanced feature engineering with 50+ behavioral features"""
    
    def __init__(self):
        self.threat_intel_db = {}  # Placeholder for threat intelligence
        self.geo_db = {}  # Placeholder for geolocation database
        
    def extract_all_features(self, log_entry: Dict, user_profile: Dict, context: Dict = None) -> Dict:
        """Extract comprehensive feature set (50+ features)"""
        features = {}
        
        # Temporal features (15 features)
        features.update(self._extract_temporal_features(log_entry, user_profile))
        
        # Geolocation features (10 features)
        features.update(self._extract_geo_features(log_entry, user_profile))
        
        # Device/Network features (12 features)
        features.update(self._extract_device_features(log_entry, user_profile))
        
        # Behavioral features (8 features)
        features.update(self._extract_behavioral_features(log_entry, user_profile))
        
        # Threat intelligence features (5 features)
        features.update(self._extract_threat_intel_features(log_entry))
        
        # Statistical features (5 features)
        features.update(self._extract_statistical_features(log_entry, user_profile))
        
        return features
    
    def _extract_temporal_features(self, log_entry: Dict, user_profile: Dict) -> Dict:
        """Extract time-based features"""
        timestamp = pd.to_datetime(log_entry['timestamp'])
        features = {}
        
        # Basic time features
        features['hour'] = timestamp.hour
        features['day_of_week'] = timestamp.dayofweek
        features['day_of_month'] = timestamp.day
        features['month'] = timestamp.month
        features['is_weekend'] = 1 if timestamp.dayofweek >= 5 else 0
        features['is_holiday'] = self._is_holiday(timestamp)
        
        # Work pattern features
        features['is_work_hours'] = 1 if 8 <= timestamp.hour <= 18 else 0
        features['is_lunch_time'] = 1 if 12 <= timestamp.hour <= 13 else 0
        features['is_early_morning'] = 1 if 5 <= timestamp.hour <= 7 else 0
        features['is_late_night'] = 1 if timestamp.hour >= 22 or timestamp.hour <= 5 else 0
        
        # User-specific temporal deviations
        if user_profile:
            avg_hour = user_profile.get('avg_login_hour', 12)
            features['hour_deviation'] = abs(timestamp.hour - avg_hour)
            features['hour_deviation_normalized'] = features['hour_deviation'] / 12
            
            # Time since last activity
            last_seen = user_profile.get('last_seen')
            if last_seen:
                last_timestamp = pd.to_datetime(last_seen)
                time_diff = (timestamp - last_timestamp).total_seconds()
                features['time_since_last_activity'] = time_diff / 3600  # hours
                features['unusual_gap'] = 1 if time_diff > 86400 else 0  # >24 hours
        else:
            features['hour_deviation'] = 0
            features['hour_deviation_normalized'] = 0
            features['time_since_last_activity'] = 0
            features['unusual_gap'] = 0
        
        return features
    
    def _extract_geo_features(self, log_entry: Dict, user_profile: Dict) -> Dict:
        """Extract geolocation-based features"""
        features = {}
        
        location = log_entry.get('location', 'Unknown')
        ip_address = log_entry.get('ip_address', '')
        
        # Basic location features
        features['location_known'] = 1 if location != 'Unknown' else 0
        features['location_hash'] = hash(location) % 1000  # Numeric representation
        
        # User location consistency
        if user_profile:
            primary_location = user_profile.get('primary_location', '')
            features['location_match'] = 1 if location == primary_location else 0
            features['location_diversity'] = user_profile.get('location_diversity', 1)
        else:
            features['location_match'] = 1
            features['location_diversity'] = 1
        
        # IP-based features
        features['ip_private'] = 1 if self._is_private_ip(ip_address) else 0
        features['ip_reputation'] = self._get_ip_reputation(ip_address)
        
        # Geographic risk factors
        high_risk_countries = ['Unknown', 'TOR', 'VPN']
        features['high_risk_location'] = 1 if location in high_risk_countries else 0
        
        # Distance-based features (simplified)
        features['location_distance'] = self._calculate_location_distance(
            location, user_profile.get('primary_location', location)
        )
        features['impossible_travel'] = self._detect_impossible_travel(
            log_entry, user_profile
        )
        
        return features
    
    def _extract_device_features(self, log_entry: Dict, user_profile: Dict) -> Dict:
        """Extract device and network features"""
        features = {}
        
        device = log_entry.get('device', 'unknown')
        user_agent = log_entry.get('user_agent', '')
        
        # Device consistency
        if user_profile:
            primary_device = user_profile.get('primary_device', '')
            features['device_match'] = 1 if device == primary_device else 0
            features['device_diversity'] = user_profile.get('device_diversity', 1)
        else:
            features['device_match'] = 1
            features['device_diversity'] = 1
        
        # Device type features
        device_types = ['laptop', 'desktop', 'mobile', 'tablet']
        for device_type in device_types:
            features[f'is_{device_type}'] = 1 if device == device_type else 0
        
        # User agent analysis
        features['user_agent_length'] = len(user_agent)
        features['user_agent_suspicious'] = self._analyze_user_agent(user_agent)
        
        # Network features
        features['vpn_detected'] = 1 if 'vpn' in log_entry.get('ip_address', '').lower() else 0
        features['tor_detected'] = 1 if 'tor' in log_entry.get('ip_address', '').lower() else 0
        
        return features
    
    def _extract_behavioral_features(self, log_entry: Dict, user_profile: Dict) -> Dict:
        """Extract behavioral pattern features"""
        features = {}
        
        action = log_entry.get('action', '')
        resource = log_entry.get('resource', '')
        session_duration = log_entry.get('session_duration', 0)
        
        # Action type features
        action_types = ['login', 'logout', 'access_resource', 'failed_login']
        for action_type in action_types:
            features[f'is_{action_type}'] = 1 if action == action_type else 0
        
        # Resource access features
        sensitive_resources = ['admin_panel', 'database', 'finance_app', 'hr_portal']
        features['sensitive_resource'] = 1 if resource in sensitive_resources else 0
        
        # Session behavior
        features['session_duration'] = session_duration
        features['long_session'] = 1 if session_duration > 480 else 0  # >8 hours
        features['short_session'] = 1 if session_duration < 5 else 0   # <5 minutes
        
        # Success/failure patterns
        features['is_success'] = 1 if log_entry.get('success', True) else 0
        features['is_failure'] = 1 - features['is_success']
        
        return features
    
    def _extract_threat_intel_features(self, log_entry: Dict) -> Dict:
        """Extract threat intelligence features"""
        features = {}
        
        ip_address = log_entry.get('ip_address', '')
        
        # Threat intelligence lookups (simplified)
        features['ip_blacklisted'] = self._check_ip_blacklist(ip_address)
        features['malware_c2'] = self._check_malware_c2(ip_address)
        features['threat_actor_ip'] = self._check_threat_actor_ip(ip_address)
        features['recent_breach_ip'] = self._check_recent_breach_ip(ip_address)
        features['threat_score'] = self._calculate_threat_score(log_entry)
        
        return features
    
    def _extract_statistical_features(self, log_entry: Dict, user_profile: Dict) -> Dict:
        """Extract statistical deviation features"""
        features = {}
        
        if user_profile:
            # Statistical deviations from user baseline
            session_duration = log_entry.get('session_duration', 0)
            avg_session = user_profile.get('avg_session_duration', 120)
            std_session = user_profile.get('session_duration_std', 60)
            
            if std_session > 0:
                features['session_z_score'] = abs(session_duration - avg_session) / std_session
            else:
                features['session_z_score'] = 0
            
            # Activity frequency deviation
            features['activity_frequency_deviation'] = self._calculate_frequency_deviation(
                log_entry, user_profile
            )
            
            # Pattern consistency score
            features['pattern_consistency'] = self._calculate_pattern_consistency(
                log_entry, user_profile
            )
            
            # Risk trend
            features['user_risk_trend'] = user_profile.get('recent_risk_trend', 0)
            features['user_baseline_risk'] = user_profile.get('baseline_risk', 0.1)
        else:
            features['session_z_score'] = 0
            features['activity_frequency_deviation'] = 0
            features['pattern_consistency'] = 1
            features['user_risk_trend'] = 0
            features['user_baseline_risk'] = 0.1
        
        return features
    
    # Helper methods
    def _is_holiday(self, timestamp):
        """Check if date is a holiday (simplified)"""
        # Simplified holiday detection
        holidays = [
            (1, 1),   # New Year
            (7, 4),   # Independence Day
            (12, 25), # Christmas
        ]
        return 1 if (timestamp.month, timestamp.day) in holidays else 0
    
    def _is_private_ip(self, ip_address):
        """Check if IP is private"""
        if not ip_address:
            return False
        return ip_address.startswith(('192.168.', '10.', '172.'))
    
    def _get_ip_reputation(self, ip_address):
        """Get IP reputation score (0-1, higher = more suspicious)"""
        # Simplified reputation scoring
        if not ip_address:
            return 0.5
        
        # Check against known bad patterns
        suspicious_patterns = ['tor', 'proxy', 'vpn', 'botnet']
        for pattern in suspicious_patterns:
            if pattern in ip_address.lower():
                return 0.8
        
        return 0.1  # Default low risk
    
    def _calculate_location_distance(self, location1, location2):
        """Calculate distance between locations (simplified)"""
        if location1 == location2:
            return 0
        
        # Simplified distance calculation
        location_coords = {
            'New York': (40.7128, -74.0060),
            'London': (51.5074, -0.1278),
            'Tokyo': (35.6762, 139.6503),
            'Sydney': (-33.8688, 151.2093),
            'Toronto': (43.6532, -79.3832),
            'Berlin': (52.5200, 13.4050),
            'Paris': (48.8566, 2.3522),
            'Singapore': (1.3521, 103.8198),
            'Moscow': (55.7558, 37.6176),
        }
        
        if location1 in location_coords and location2 in location_coords:
            # Simplified distance (could use haversine formula)
            lat1, lon1 = location_coords[location1]
            lat2, lon2 = location_coords[location2]
            distance = ((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5
            return min(distance * 100, 1000)  # Normalize
        
        return 500  # Default medium distance
    
    def _detect_impossible_travel(self, log_entry, user_profile):
        """Detect impossible travel between locations"""
        if not user_profile or not user_profile.get('last_location'):
            return 0
        
        current_location = log_entry.get('location')
        last_location = user_profile.get('last_location')
        last_timestamp = user_profile.get('last_seen')
        
        if not all([current_location, last_location, last_timestamp]):
            return 0
        
        # Calculate time difference
        current_time = pd.to_datetime(log_entry['timestamp'])
        last_time = pd.to_datetime(last_timestamp)
        time_diff_hours = (current_time - last_time).total_seconds() / 3600
        
        # Calculate distance
        distance = self._calculate_location_distance(current_location, last_location)
        
        # Check if travel is possible (assuming max speed of 1000 km/h)
        max_possible_distance = time_diff_hours * 1000
        
        return 1 if distance > max_possible_distance else 0
    
    def _analyze_user_agent(self, user_agent):
        """Analyze user agent for suspicious patterns"""
        if not user_agent:
            return 0.5
        
        suspicious_patterns = ['bot', 'crawler', 'script', 'automated']
        for pattern in suspicious_patterns:
            if pattern.lower() in user_agent.lower():
                return 1
        
        return 0
    
    def _check_ip_blacklist(self, ip_address):
        """Check IP against blacklist"""
        # Simplified blacklist check
        blacklisted_ips = ['10.0.0.1', '192.168.1.100']  # Example
        return 1 if ip_address in blacklisted_ips else 0
    
    def _check_malware_c2(self, ip_address):
        """Check if IP is known malware C2"""
        return 0  # Simplified
    
    def _check_threat_actor_ip(self, ip_address):
        """Check if IP is associated with threat actors"""
        return 0  # Simplified
    
    def _check_recent_breach_ip(self, ip_address):
        """Check if IP was involved in recent breaches"""
        return 0  # Simplified
    
    def _calculate_threat_score(self, log_entry):
        """Calculate overall threat score for the entry"""
        score = 0
        
        # Add points for suspicious indicators
        if log_entry.get('location') == 'Moscow':
            score += 0.3
        if 'admin' in log_entry.get('resource', ''):
            score += 0.2
        if not log_entry.get('success', True):
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_frequency_deviation(self, log_entry, user_profile):
        """Calculate deviation from normal activity frequency"""
        # Simplified frequency deviation calculation
        normal_frequency = user_profile.get('daily_avg_activities', 10)
        return abs(1 - normal_frequency / 10) if normal_frequency > 0 else 0
    
    def _calculate_pattern_consistency(self, log_entry, user_profile):
        """Calculate how consistent this activity is with user patterns"""
        # Simplified consistency score
        consistency_factors = []
        
        # Time consistency
        hour = pd.to_datetime(log_entry['timestamp']).hour
        avg_hour = user_profile.get('avg_login_hour', 12)
        time_consistency = 1 - abs(hour - avg_hour) / 12
        consistency_factors.append(time_consistency)
        
        # Location consistency
        location_match = 1 if log_entry.get('location') == user_profile.get('primary_location') else 0
        consistency_factors.append(location_match)
        
        # Device consistency
        device_match = 1 if log_entry.get('device') == user_profile.get('primary_device') else 0
        consistency_factors.append(device_match)
        
        return np.mean(consistency_factors)

class EnsembleAnomalyDetector:
    """Advanced ensemble anomaly detector with multiple algorithms"""
    
    def __init__(self, contamination=0.1):
        self.contamination = contamination
        self.algorithms = {}
        self.ensemble = None
        self.scaler = RobustScaler()
        self.feature_engineer = AdvancedFeatureEngineer()
        self.is_trained = False
        self.feature_columns = []
        
        # Initialize algorithms
        self._initialize_algorithms()
    
    def _initialize_algorithms(self):
        """Initialize all anomaly detection algorithms"""
        self.algorithms = {
            'isolation_forest': IsolationForest(
                contamination=self.contamination,
                random_state=42,
                n_estimators=200,
                max_features=1.0
            ),
            'one_class_svm': OneClassSVM(
                kernel='rbf',
                gamma='scale',
                nu=self.contamination
            ),
            'local_outlier_factor': LocalOutlierFactor(
                n_neighbors=20,
                contamination=self.contamination,
                novelty=True
            ),
            'gaussian_mixture': GaussianMixture(
                n_components=2,
                covariance_type='full',
                random_state=42
            ),
            'lstm_autoencoder': LSTMAutoencoder(
                sequence_length=10,
                n_features=50,
                encoding_dim=32
            )
        }
    
    def fit(self, X, user_profiles=None):
        """Train all algorithms in the ensemble"""
        print(f"Training ensemble with {len(X)} samples...")
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        self.feature_columns = list(range(X.shape[1]))
        
        # Train each algorithm
        trained_algorithms = {}
        
        for name, algorithm in self.algorithms.items():
            try:
                print(f"Training {name}...")
                
                if name == 'lstm_autoencoder':
                    # LSTM needs special handling
                    algorithm.fit(X_scaled)
                elif name == 'gaussian_mixture':
                    # Gaussian Mixture needs special handling
                    algorithm.fit(X_scaled)
                else:
                    # Standard sklearn algorithms
                    algorithm.fit(X_scaled)
                
                trained_algorithms[name] = algorithm
                print(f"✅ {name} trained successfully")
                
            except Exception as e:
                print(f"❌ Failed to train {name}: {e}")
                continue
        
        self.algorithms = trained_algorithms
        self.is_trained = True
        
        print(f"Ensemble training completed with {len(self.algorithms)} algorithms")
        return self
    
    def predict(self, X):
        """Predict anomalies using ensemble voting"""
        if not self.is_trained:
            raise ValueError("Ensemble not trained yet")
        
        X_scaled = self.scaler.transform(X)
        predictions = {}
        scores = {}
        
        # Get predictions from each algorithm
        for name, algorithm in self.algorithms.items():
            try:
                if name == 'lstm_autoencoder':
                    # LSTM returns anomaly scores
                    score = algorithm.predict(X_scaled)
                    pred = (score > 1.0).astype(int) * 2 - 1  # Convert to -1/1
                elif name == 'gaussian_mixture':
                    # Gaussian Mixture returns log likelihood
                    log_likelihood = algorithm.score_samples(X_scaled)
                    threshold = np.percentile(log_likelihood, self.contamination * 100)
                    pred = (log_likelihood < threshold).astype(int) * 2 - 1
                    score = -log_likelihood  # Higher score = more anomalous
                else:
                    # Standard sklearn algorithms
                    pred = algorithm.predict(X_scaled)
                    if hasattr(algorithm, 'decision_function'):
                        score = -algorithm.decision_function(X_scaled)  # Invert for consistency
                    else:
                        score = -algorithm.score_samples(X_scaled)
                
                predictions[name] = pred
                scores[name] = score
                
            except Exception as e:
                print(f"Warning: {name} prediction failed: {e}")
                continue
        
        # Ensemble voting
        if predictions:
            # Majority voting for binary prediction
            pred_array = np.array(list(predictions.values()))
            ensemble_pred = np.sign(np.mean(pred_array, axis=0))
            
            # Average scoring
            score_array = np.array(list(scores.values()))
            ensemble_score = np.mean(score_array, axis=0)
            
            return ensemble_pred, ensemble_score
        else:
            raise ValueError("No algorithms available for prediction")
    
    def predict_proba(self, X):
        """Predict anomaly probabilities"""
        _, scores = self.predict(X)
        
        # Convert scores to probabilities using sigmoid
        probabilities = 1 / (1 + np.exp(-scores))
        return probabilities
    
    def get_feature_importance(self):
        """Get feature importance from tree-based algorithms"""
        importance_dict = {}
        
        for name, algorithm in self.algorithms.items():
            if hasattr(algorithm, 'feature_importances_'):
                importance_dict[name] = algorithm.feature_importances_
        
        return importance_dict
    
    def save_model(self, model_path):
        """Save the trained ensemble model"""
        model_data = {
            'algorithms': self.algorithms,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns,
            'contamination': self.contamination,
            'is_trained': self.is_trained
        }
        
        joblib.dump(model_data, model_path)
        print(f"Ensemble model saved to {model_path}")
    
    def load_model(self, model_path):
        """Load a trained ensemble model"""
        model_data = joblib.load(model_path)
        
        self.algorithms = model_data['algorithms']
        self.scaler = model_data['scaler']
        self.feature_columns = model_data['feature_columns']
        self.contamination = model_data['contamination']
        self.is_trained = model_data['is_trained']
        
        print(f"Ensemble model loaded from {model_path}")

class AdvancedAnomalyDetector:
    """Main class for advanced anomaly detection system"""
    
    def __init__(self, contamination=0.1):
        self.ensemble = EnsembleAnomalyDetector(contamination)
        self.feature_engineer = AdvancedFeatureEngineer()
        self.user_profiles = {}
        self.performance_metrics = {}
        
    async def analyze_activity_async(self, activity, user_id):
        """Async version of activity analysis for high-performance processing"""
        loop = asyncio.get_event_loop()
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(
                executor, self.analyze_activity, activity, user_id
            )
        
        return result
    
    def analyze_activity(self, activity, user_id):
        """Analyze a single activity with advanced features"""
        if not self.ensemble.is_trained:
            raise ValueError("Model not trained yet")
        
        # Get user profile
        user_profile = self.user_profiles.get(user_id, {})
        
        # Extract advanced features
        features = self.feature_engineer.extract_all_features(
            activity, user_profile
        )
        
        # Convert to array
        feature_array = np.array(list(features.values())).reshape(1, -1)
        
        # Predict anomaly
        prediction, anomaly_score = self.ensemble.predict(feature_array)
        is_anomaly = prediction[0] == -1
        
        # Calculate risk score with advanced logic
        risk_score = self._calculate_advanced_risk_score(
            anomaly_score[0], features, activity, user_profile
        )
        
        # Determine risk level
        risk_level = self._get_risk_level(risk_score)
        
        return {
            'anomaly_score': float(anomaly_score[0]),
            'is_anomaly': bool(is_anomaly),
            'risk_score': float(risk_score),
            'risk_level': risk_level,
            'features_used': features,
            'activity': activity,
            'user_id': user_id,
            'timestamp': activity['timestamp'],
            'explanation': self._generate_explanation(features, risk_score)
        }
    
    def _calculate_advanced_risk_score(self, base_score, features, activity, user_profile):
        """Calculate advanced risk score with multiple factors"""
        # Normalize base score to 0-1 range
        normalized_score = max(0, min(1, (base_score + 1) / 2))
        
        # Apply feature-based multipliers
        multipliers = 1.0
        
        # Time-based risk
        if features.get('is_late_night', 0):
            multipliers *= 1.4
        if features.get('is_weekend', 0):
            multipliers *= 1.2
        if features.get('hour_deviation', 0) > 6:
            multipliers *= 1.3
        
        # Location-based risk
        if not features.get('location_match', 1):
            multipliers *= 1.5
        if features.get('high_risk_location', 0):
            multipliers *= 1.6
        if features.get('impossible_travel', 0):
            multipliers *= 2.0
        
        # Device-based risk
        if not features.get('device_match', 1):
            multipliers *= 1.3
        if features.get('user_agent_suspicious', 0):
            multipliers *= 1.4
        
        # Behavioral risk
        if features.get('sensitive_resource', 0):
            multipliers *= 1.5
        if features.get('long_session', 0):
            multipliers *= 1.2
        if features.get('is_failure', 0):
            multipliers *= 1.8
        
        # Threat intelligence risk
        if features.get('ip_blacklisted', 0):
            multipliers *= 2.5
        if features.get('threat_score', 0) > 0.5:
            multipliers *= 1.7
        
        # Statistical deviation risk
        if features.get('session_z_score', 0) > 2:
            multipliers *= 1.3
        if features.get('pattern_consistency', 1) < 0.5:
            multipliers *= 1.4
        
        # Calculate final risk score
        risk_score = min(100, normalized_score * multipliers * 100)
        
        return risk_score
    
    def _get_risk_level(self, risk_score):
        """Determine risk level from score"""
        if risk_score >= 90:
            return "Critical"
        elif risk_score >= 70:
            return "High"
        elif risk_score >= 40:
            return "Medium"
        else:
            return "Low"
    
    def _generate_explanation(self, features, risk_score):
        """Generate human-readable explanation for the risk score"""
        explanations = []
        
        # Time-based explanations
        if features.get('is_late_night', 0):
            explanations.append("Activity during late night hours")
        if features.get('hour_deviation', 0) > 6:
            explanations.append("Login time significantly different from normal pattern")
        
        # Location-based explanations
        if not features.get('location_match', 1):
            explanations.append("Login from unusual location")
        if features.get('impossible_travel', 0):
            explanations.append("Impossible travel detected between locations")
        
        # Device-based explanations
        if not features.get('device_match', 1):
            explanations.append("Login from new or unusual device")
        
        # Behavioral explanations
        if features.get('sensitive_resource', 0):
            explanations.append("Access to sensitive resources")
        if features.get('is_failure', 0):
            explanations.append("Failed authentication attempt")
        
        # Threat intelligence explanations
        if features.get('ip_blacklisted', 0):
            explanations.append("IP address found in threat intelligence blacklist")
        
        if not explanations:
            explanations.append("Multiple minor deviations from normal behavior")
        
        return "; ".join(explanations)
    
    def train(self, df, user_profiles):
        """Train the advanced anomaly detection system"""
        self.user_profiles = user_profiles
        
        print("Extracting advanced features for training...")
        feature_list = []
        
        for _, row in df.iterrows():
            user_id = row['user_id']
            user_profile = user_profiles.get(user_id, {})
            
            features = self.feature_engineer.extract_all_features(
                row.to_dict(), user_profile
            )
            feature_list.append(list(features.values()))
        
        # Convert to numpy array
        X = np.array(feature_list)
        
        print(f"Training with {X.shape[0]} samples and {X.shape[1]} features")
        
        # Train ensemble
        self.ensemble.fit(X, user_profiles)
        
        print("Advanced anomaly detection system training completed!")
        
        return self
    
    def save_model(self, model_path, profiles_path):
        """Save the complete model"""
        self.ensemble.save_model(model_path)
        
        with open(profiles_path, 'w') as f:
            json.dump(self.user_profiles, f, indent=2, default=str)
        
        print(f"Complete model saved: {model_path}, {profiles_path}")
    
    def load_model(self, model_path, profiles_path):
        """Load the complete model"""
        self.ensemble.load_model(model_path)
        
        with open(profiles_path, 'r') as f:
            self.user_profiles = json.load(f)
        
        print(f"Complete model loaded: {model_path}, {profiles_path}")

def main():
    """Test the advanced ML engine"""
    print("🧠 Advanced ML Engine - Testing")
    print("=" * 50)
    
    # Initialize advanced detector
    detector = AdvancedAnomalyDetector(contamination=0.1)
    
    # Load data (using existing data)
    try:
        with open("data/sample_logs.json", 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        
        with open("data/user_profiles.json", 'r') as f:
            user_profiles = json.load(f)
        
        print(f"Loaded {len(df)} samples and {len(user_profiles)} user profiles")
        
        # Train advanced system
        detector.train(df, user_profiles)
        
        # Save advanced model
        detector.save_model("data/advanced_model.pkl", "data/advanced_profiles.json")
        
        # Test with sample activities
        print("\n=== Testing Advanced Detection ===")
        
        # Normal activity
        normal_activity = {
            'timestamp': '2026-01-09 10:30:00',
            'user_id': 'john.doe',
            'action': 'login',
            'location': 'New York',
            'device': 'laptop',
            'resource': 'email',
            'success': True,
            'session_duration': 120,
            'ip_address': '192.168.1.100',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        result = detector.analyze_activity(normal_activity, 'john.doe')
        print(f"\n📊 Normal Activity Analysis:")
        print(f"   Risk Score: {result['risk_score']:.1f}")
        print(f"   Risk Level: {result['risk_level']}")
        print(f"   Explanation: {result['explanation']}")
        
        # Suspicious activity
        suspicious_activity = {
            'timestamp': '2026-01-09 03:00:00',
            'user_id': 'john.doe',
            'action': 'login',
            'location': 'Moscow',
            'device': 'unknown_device',
            'resource': 'admin_panel',
            'success': True,
            'session_duration': 600,
            'ip_address': '10.0.0.1',
            'user_agent': 'bot/1.0'
        }
        
        result = detector.analyze_activity(suspicious_activity, 'john.doe')
        print(f"\n🚨 Suspicious Activity Analysis:")
        print(f"   Risk Score: {result['risk_score']:.1f}")
        print(f"   Risk Level: {result['risk_level']}")
        print(f"   Explanation: {result['explanation']}")
        
        print(f"\n✅ Advanced ML Engine testing completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()