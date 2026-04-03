#!/usr/bin/env python3
"""
Dataset Analyzer - Categorize datasets into Risk/No-Risk
This allows users to upload custom datasets for analysis
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import json
from datetime import datetime
from typing import Dict, List, Tuple, Any

class DatasetAnalyzer:
    """
    Analyze custom datasets and categorize activities as Risk/No-Risk
    """
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.label_encoders = {}
        self.feature_columns = []
        self.is_trained = False
        
    def load_dataset(self, file_path: str) -> Dict:
        """Load dataset from various formats"""
        try:
            # Try different file formats
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.json'):
                df = pd.read_json(file_path)
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                return {'error': 'Unsupported file format. Use CSV, JSON, or XLSX'}
            
            # Validate required columns
            required_columns = ['user_id', 'timestamp', 'action', 'location', 'device']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return {'error': f'Missing required columns: {missing_columns}'}
            
            return {
                'success': True,
                'data': df,
                'shape': df.shape,
                'columns': list(df.columns)
            }
            
        except Exception as e:
            return {'error': f'Failed to load dataset: {str(e)}'}
    
    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocess dataset for ML analysis"""
        df_processed = df.copy()
        
        # Convert timestamp
        df_processed['timestamp'] = pd.to_datetime(df_processed['timestamp'])
        df_processed['hour'] = df_processed['timestamp'].dt.hour
        df_processed['day_of_week'] = df_processed['timestamp'].dt.dayofweek
        df_processed['is_weekend'] = (df_processed['day_of_week'] >= 5).astype(int)
        df_processed['is_off_hours'] = ((df_processed['hour'] < 8) | (df_processed['hour'] > 18)).astype(int)
        
        # Encode categorical variables
        categorical_columns = ['user_id', 'action', 'location', 'device', 'resource', 'user_agent']
        
        for col in categorical_columns:
            if col in df_processed.columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                df_processed[f'{col}_encoded'] = self.label_encoders[col].fit_transform(df_processed[col].astype(str))
        
        # Create feature columns
        feature_columns = []
        for col in ['hour', 'day_of_week', 'is_weekend', 'is_off_hours']:
            if col in df_processed.columns:
                feature_columns.append(col)
        
        for col in categorical_columns:
            encoded_col = f'{col}_encoded'
            if encoded_col in df_processed.columns:
                feature_columns.append(encoded_col)
        
        # Add numerical features
        if 'session_duration' in df_processed.columns:
            df_processed['session_duration'] = df_processed['session_duration'].fillna(60)
            feature_columns.append('session_duration')
        
        if 'success' in df_processed.columns:
            df_processed['success'] = df_processed['success'].fillna(True).astype(int)
            feature_columns.append('success')
        else:
            df_processed['success'] = 1  # Default to success
            feature_columns.append('success')
        
        self.feature_columns = feature_columns
        return df_processed
    
    def train_anomaly_detector(self, df: pd.DataFrame) -> Dict:
        """Train anomaly detection model"""
        try:
            # Preprocess data
            df_processed = self.preprocess_data(df)
            
            # Prepare features
            X = df_processed[self.feature_columns]
            
            # Scale features
            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(X)
            
            # Train Isolation Forest
            self.model = IsolationForest(
                contamination=0.1,  # Assume 10% anomalies
                random_state=42,
                n_estimators=100
            )
            
            # Fit model
            self.model.fit(X_scaled)
            
            # Get predictions and scores
            predictions = self.model.predict(X_scaled)
            scores = self.model.decision_function(X_scaled)
            
            # Add predictions to dataframe
            df_processed['is_anomaly'] = predictions == -1
            df_processed['anomaly_score'] = scores
            df_processed['risk_category'] = np.where(
                df_processed['is_anomaly'], 
                'Risk', 
                'No-Risk'
            )
            
            self.is_trained = True
            
            # Calculate statistics
            total_records = len(df_processed)
            risk_count = df_processed['is_anomaly'].sum()
            no_risk_count = total_records - risk_count
            risk_percentage = (risk_count / total_records) * 100
            
            return {
                'success': True,
                'model_trained': True,
                'total_records': int(total_records),
                'risk_records': int(risk_count),
                'no_risk_records': int(no_risk_count),
                'risk_percentage': round(risk_percentage, 2),
                'feature_columns': self.feature_columns,
                'data_with_predictions': df_processed.to_dict('records')
            }
            
        except Exception as e:
            return {'error': f'Training failed: {str(e)}'}
    
    def analyze_new_data(self, new_data: List[Dict]) -> Dict:
        """Analyze new dataset using trained model"""
        if not self.is_trained:
            return {'error': 'Model not trained. Please train on a dataset first.'}
        
        try:
            # Convert to DataFrame
            df_new = pd.DataFrame(new_data)
            
            # Preprocess using same transformations
            df_processed = self.preprocess_data(df_new)
            
            # Prepare features
            X = df_processed[self.feature_columns]
            
            # Scale using existing scaler
            X_scaled = self.scaler.transform(X)
            
            # Get predictions
            predictions = self.model.predict(X_scaled)
            scores = self.model.decision_function(X_scaled)
            
            # Add predictions
            df_processed['is_anomaly'] = predictions == -1
            df_processed['anomaly_score'] = scores
            df_processed['risk_category'] = np.where(
                df_processed['is_anomaly'], 
                'Risk', 
                'No-Risk'
            )
            
            # Convert back to original format
            results = []
            for i, row in df_processed.iterrows():
                result = {
                    'original_data': new_data[i],
                    'risk_category': row['risk_category'],
                    'anomaly_score': round(float(row['anomaly_score']), 3),
                    'is_anomaly': bool(row['is_anomaly']),
                    'confidence': abs(float(row['anomaly_score']))
                }
                results.append(result)
            
            # Calculate summary
            risk_count = sum(1 for r in results if r['risk_category'] == 'Risk')
            total_count = len(results)
            risk_percentage = (risk_count / total_count) * 100
            
            return {
                'success': True,
                'total_analyzed': int(total_count),
                'risk_count': int(risk_count),
                'no_risk_count': int(total_count - risk_count),
                'risk_percentage': round(risk_percentage, 2),
                'results': results
            }
            
        except Exception as e:
            return {'error': f'Analysis failed: {str(e)}'}
    
    def generate_sample_dataset(self, num_records: int = 1000) -> pd.DataFrame:
        """Generate sample dataset for testing"""
        np.random.seed(42)
        
        users = ['alice', 'bob', 'charlie', 'diana', 'eve']
        locations = ['New York', 'London', 'Tokyo', 'Moscow', 'Unknown']
        devices = ['laptop', 'desktop', 'mobile', 'unknown_device']
        actions = ['login', 'logout', 'access_resource', 'download']
        resources = ['email', 'database', 'admin_panel', 'file_server']
        
        data = []
        for i in range(num_records):
            # Generate mostly normal data (90%)
            if np.random.random() < 0.9:
                # Normal activity
                user = np.random.choice(users)
                location = np.random.choice(['New York', 'London', 'Tokyo'])
                device = np.random.choice(['laptop', 'desktop'])
                hour = np.random.randint(8, 19)
                action = np.random.choice(['login', 'access_resource'])
            else:
                # Anomalous activity
                user = np.random.choice(users)
                location = np.random.choice(['Moscow', 'Unknown'])
                device = np.random.choice(['unknown_device', 'mobile'])
                hour = np.random.randint(0, 24)
                action = np.random.choice(['login', 'access_resource'])
            
            record = {
                'user_id': user,
                'timestamp': f'2026-01-{np.random.randint(1, 29):02d} {hour:02d}:{np.random.randint(0, 60):02d}',
                'action': action,
                'location': location,
                'device': device,
                'resource': np.random.choice(resources),
                'session_duration': np.random.randint(30, 480),
                'success': np.random.choice([True, False], p=[0.95, 0.05]),
                'ip_address': f'192.168.1.{np.random.randint(1, 255)}',
                'user_agent': 'Mozilla/5.0' if device != 'unknown_device' else 'bot/1.0'
            }
            data.append(record)
        
        return pd.DataFrame(data)
    
    def get_model_summary(self) -> Dict:
        """Get summary of trained model"""
        if not self.is_trained:
            return {'error': 'Model not trained'}
        
        return {
            'model_type': 'Isolation Forest',
            'feature_columns': self.feature_columns,
            'label_encoders': list(self.label_encoders.keys()),
            'is_trained': self.is_trained,
            'contamination_rate': 0.1
        }
