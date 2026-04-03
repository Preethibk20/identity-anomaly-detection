import pandas as pd
import numpy as np
import json
from datetime import datetime
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(
            contamination=0.1,  # Expect 10% anomalies
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.feature_columns = []
        self.is_trained = False
        self.user_profiles = {}
    
    def load_user_profiles(self, file_path):
        """Load user behavioral profiles"""
        with open(file_path, 'r') as f:
            self.user_profiles = json.load(f)
    
    def extract_activity_features(self, activity, user_profile):
        """Extract features from a single activity for anomaly detection"""
        features = {}
        
        # Parse timestamp
        timestamp = pd.to_datetime(activity['timestamp'])
        hour = timestamp.hour
        day_of_week = timestamp.dayofweek
        
        # Temporal features
        features['hour'] = hour
        features['is_weekend'] = 1 if day_of_week >= 5 else 0
        features['is_off_hours'] = 1 if hour < 8 or hour > 18 else 0
        features['is_night'] = 1 if hour < 6 or hour > 22 else 0
        
        # Deviation from user's normal pattern
        if user_profile:
            avg_hour = user_profile.get('avg_login_hour', 12)
            features['hour_deviation'] = abs(hour - avg_hour)
            
            # Location consistency
            primary_location = user_profile.get('primary_location', '')
            features['location_match'] = 1 if activity['location'] == primary_location else 0
            
            # Device consistency
            primary_device = user_profile.get('primary_device', '')
            features['device_match'] = 1 if activity['device'] == primary_device else 0
            
            # Work hours consistency
            work_hours_ratio = user_profile.get('work_hours_ratio', 0.8)
            features['work_pattern_deviation'] = abs(features['is_off_hours'] - (1 - work_hours_ratio))
        else:
            # Default values if no profile available
            features['hour_deviation'] = 0
            features['location_match'] = 1
            features['device_match'] = 1
            features['work_pattern_deviation'] = 0
        
        # Activity-specific features
        features['is_login'] = 1 if activity['action'] == 'login' else 0
        features['is_failed'] = 1 if not activity.get('success', True) else 0
        
        # Session duration (if available)
        session_duration = activity.get('session_duration', 60)
        features['session_duration'] = session_duration
        features['long_session'] = 1 if session_duration > 240 else 0  # > 4 hours
        
        # Resource sensitivity (simple scoring)
        sensitive_resources = ['admin_panel', 'database', 'finance_app']
        features['sensitive_resource'] = 1 if activity.get('resource', '') in sensitive_resources else 0
        
        return features
    
    def prepare_training_data(self, df):
        """Prepare feature matrix for training"""
        features_list = []
        
        for _, activity in df.iterrows():
            user_id = activity['user_id']
            user_profile = self.user_profiles.get(user_id, {})
            
            activity_features = self.extract_activity_features(activity.to_dict(), user_profile)
            features_list.append(activity_features)
        
        # Convert to DataFrame
        features_df = pd.DataFrame(features_list)
        self.feature_columns = features_df.columns.tolist()
        
        return features_df
    
    def train(self, df):
        """Train the anomaly detection model"""
        print("Preparing training data...")
        features_df = self.prepare_training_data(df)
        
        print(f"Training with {len(features_df)} samples and {len(self.feature_columns)} features")
        print(f"Features: {self.feature_columns}")
        
        # Scale features
        features_scaled = self.scaler.fit_transform(features_df)
        
        # Train model
        self.model.fit(features_scaled)
        self.is_trained = True
        
        print("Model training completed!")
        
        # Show training statistics
        anomaly_scores = self.model.decision_function(features_scaled)
        predictions = self.model.predict(features_scaled)
        
        print(f"Training anomalies detected: {(predictions == -1).sum()} out of {len(predictions)}")
        print(f"Anomaly score range: {anomaly_scores.min():.3f} to {anomaly_scores.max():.3f}")
    
    def predict_anomaly(self, activity, user_id):
        """Predict if an activity is anomalous"""
        if not self.is_trained:
            raise ValueError("Model not trained yet!")
        
        user_profile = self.user_profiles.get(user_id, {})
        features = self.extract_activity_features(activity, user_profile)
        
        # Convert to DataFrame with same columns as training
        features_df = pd.DataFrame([features])
        
        # Ensure all training columns are present
        for col in self.feature_columns:
            if col not in features_df.columns:
                features_df[col] = 0
        
        # Reorder columns to match training
        features_df = features_df[self.feature_columns]
        
        # Scale features
        features_scaled = self.scaler.transform(features_df)
        
        # Predict
        anomaly_score = self.model.decision_function(features_scaled)[0]
        is_anomaly = self.model.predict(features_scaled)[0] == -1
        
        return anomaly_score, is_anomaly
    
    def calculate_risk_score(self, anomaly_score, activity, user_id):
        """Calculate risk score from anomaly score and context"""
        # Normalize anomaly score to 0-1 range (roughly)
        # Isolation Forest scores are typically between -0.5 and 0.5
        normalized_score = max(0, min(1, (0.5 - anomaly_score)))
        
        # Apply context multipliers
        risk_multiplier = 1.0
        
        # Time-based risk
        timestamp = pd.to_datetime(activity['timestamp'])
        hour = timestamp.hour
        if hour < 6 or hour > 22:
            risk_multiplier *= 1.5  # Night activity
        
        # Location risk
        user_profile = self.user_profiles.get(user_id, {})
        primary_location = user_profile.get('primary_location', '')
        if activity['location'] != primary_location:
            risk_multiplier *= 1.4  # New location
        
        # Failed attempts
        if not activity.get('success', True):
            risk_multiplier *= 1.6
        
        # Sensitive resources
        sensitive_resources = ['admin_panel', 'database', 'finance_app']
        if activity.get('resource', '') in sensitive_resources:
            risk_multiplier *= 1.3
        
        # Calculate final risk score (0-100)
        risk_score = min(100, normalized_score * risk_multiplier * 100)
        
        return risk_score
    
    def analyze_activity(self, activity, user_id):
        """Complete analysis of an activity"""
        anomaly_score, is_anomaly = self.predict_anomaly(activity, user_id)
        risk_score = self.calculate_risk_score(anomaly_score, activity, user_id)
        
        # Determine risk level
        if risk_score < 30:
            risk_level = "Low"
        elif risk_score < 60:
            risk_level = "Medium"
        elif risk_score < 80:
            risk_level = "High"
        else:
            risk_level = "Critical"
        
        return {
            'anomaly_score': anomaly_score,
            'is_anomaly': is_anomaly,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'activity': activity,
            'user_id': user_id,
            'timestamp': activity['timestamp']
        }
    
    def save_model(self, model_path, scaler_path):
        """Save trained model and scaler"""
        joblib.dump(self.model, model_path)
        joblib.dump(self.scaler, scaler_path)
        
        # Save feature columns
        with open('data/feature_columns.json', 'w') as f:
            json.dump(self.feature_columns, f)
    
    def load_model(self, model_path, scaler_path):
        """Load trained model and scaler"""
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        
        # Load feature columns
        with open('data/feature_columns.json', 'r') as f:
            self.feature_columns = json.load(f)
        
        self.is_trained = True

def main():
    detector = AnomalyDetector()
    
    print("Loading user profiles...")
    detector.load_user_profiles("data/user_profiles.json")
    
    print("Loading authentication logs...")
    with open("data/sample_logs.json", 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    
    print("Training anomaly detection model...")
    detector.train(df)
    
    # Save the trained model
    detector.save_model("data/anomaly_model.pkl", "data/scaler.pkl")
    print("Model saved!")
    
    # Test on some recent activities
    print("\n=== Testing Anomaly Detection ===")
    recent_activities = df.tail(10)
    
    for _, activity in recent_activities.iterrows():
        result = detector.analyze_activity(activity.to_dict(), activity['user_id'])
        
        print(f"\nUser: {result['user_id']}")
        print(f"Time: {result['timestamp']}")
        print(f"Action: {result['activity']['action']} - {result['activity']['location']}")
        print(f"Risk Score: {result['risk_score']:.1f} ({result['risk_level']})")
        print(f"Anomaly: {'Yes' if result['is_anomaly'] else 'No'}")

if __name__ == "__main__":
    main()