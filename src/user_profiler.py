import pandas as pd
import json
import numpy as np
from datetime import datetime
from collections import defaultdict, Counter

class UserProfiler:
    def __init__(self):
        self.user_profiles = {}
    
    def load_data(self, file_path):
        """Load authentication logs from JSON file"""
        with open(file_path, 'r') as f:
            data = json.load(f)
        return pd.DataFrame(data)
    
    def extract_features(self, user_data):
        """Extract behavioral features for a user"""
        features = {}
        
        # Convert timestamp to datetime
        user_data['datetime'] = pd.to_datetime(user_data['timestamp'])
        user_data['hour'] = user_data['datetime'].dt.hour
        user_data['day_of_week'] = user_data['datetime'].dt.dayofweek
        
        # Temporal features
        features['avg_login_hour'] = user_data['hour'].mean()
        features['login_hour_std'] = user_data['hour'].std() if len(user_data) > 1 else 0
        features['most_common_hours'] = user_data['hour'].mode().tolist()[:3]  # Limit to top 3
        
        # Work pattern features
        work_hours = user_data[(user_data['hour'] >= 8) & (user_data['hour'] <= 18)]
        features['work_hours_ratio'] = len(work_hours) / len(user_data) if len(user_data) > 0 else 0
        
        # Weekend activity
        weekend_activity = user_data[user_data['day_of_week'].isin([5, 6])]
        features['weekend_activity_ratio'] = len(weekend_activity) / len(user_data) if len(user_data) > 0 else 0
        
        # Location features
        location_counts = user_data['location'].value_counts()
        features['primary_location'] = location_counts.index[0] if len(location_counts) > 0 else "Unknown"
        features['location_diversity'] = len(location_counts)
        features['primary_location_ratio'] = location_counts.iloc[0] / len(user_data) if len(location_counts) > 0 else 0
        
        # Device features
        device_counts = user_data['device'].value_counts()
        features['primary_device'] = device_counts.index[0] if len(device_counts) > 0 else "Unknown"
        features['device_diversity'] = len(device_counts)
        
        # Resource access features
        resource_counts = user_data['resource'].value_counts()
        features['resource_diversity'] = len(resource_counts)
        features['most_accessed_resources'] = resource_counts.head(3).index.tolist()
        
        # Session features
        if 'session_duration' in user_data.columns:
            features['avg_session_duration'] = user_data['session_duration'].mean()
            features['session_duration_std'] = user_data['session_duration'].std() if len(user_data) > 1 else 0
        
        # Success rate
        if 'success' in user_data.columns:
            features['success_rate'] = user_data['success'].mean()
            features['failed_attempts'] = (~user_data['success']).sum()
        
        # Activity frequency
        features['daily_avg_activities'] = len(user_data) / user_data['datetime'].dt.date.nunique()
        
        return features
    
    def create_user_profiles(self, df):
        """Create behavioral profiles for all users"""
        profiles = {}
        
        for user_id in df['user_id'].unique():
            user_data = df[df['user_id'] == user_id].copy()
            
            if len(user_data) > 5:  # Only profile users with sufficient data
                profile = self.extract_features(user_data)
                profile['total_activities'] = len(user_data)
                profile['first_seen'] = user_data['timestamp'].min()
                profile['last_seen'] = user_data['timestamp'].max()
                
                profiles[user_id] = profile
        
        self.user_profiles = profiles
        return profiles
    
    def get_user_baseline(self, user_id):
        """Get baseline profile for a specific user"""
        return self.user_profiles.get(user_id, {})
    
    def save_profiles(self, file_path):
        """Save user profiles to JSON file"""
        # Convert numpy types to Python types for JSON serialization
        serializable_profiles = {}
        for user_id, profile in self.user_profiles.items():
            serializable_profile = {}
            for key, value in profile.items():
                if isinstance(value, np.ndarray):
                    serializable_profile[key] = value.tolist()
                elif isinstance(value, (np.integer, np.floating)):
                    serializable_profile[key] = value.item()
                elif isinstance(value, list):
                    # Handle lists that might contain numpy types
                    serializable_profile[key] = [
                        item.item() if isinstance(item, (np.integer, np.floating)) else item 
                        for item in value
                    ]
                elif pd.isna(value) if not isinstance(value, (list, np.ndarray)) else False:
                    serializable_profile[key] = None
                else:
                    serializable_profile[key] = value
            serializable_profiles[user_id] = serializable_profile
        
        with open(file_path, 'w') as f:
            json.dump(serializable_profiles, f, indent=2)
    
    def load_profiles(self, file_path):
        """Load user profiles from JSON file"""
        with open(file_path, 'r') as f:
            self.user_profiles = json.load(f)
        return self.user_profiles
    
    def print_user_summary(self, user_id):
        """Print a summary of user's behavioral profile"""
        if user_id not in self.user_profiles:
            print(f"No profile found for user: {user_id}")
            return
        
        profile = self.user_profiles[user_id]
        
        print(f"\n=== User Profile: {user_id} ===")
        print(f"Total Activities: {profile.get('total_activities', 0)}")
        print(f"Average Login Hour: {profile.get('avg_login_hour', 0):.1f}")
        print(f"Work Hours Ratio: {profile.get('work_hours_ratio', 0):.2%}")
        print(f"Weekend Activity: {profile.get('weekend_activity_ratio', 0):.2%}")
        print(f"Primary Location: {profile.get('primary_location', 'Unknown')}")
        print(f"Primary Device: {profile.get('primary_device', 'Unknown')}")
        print(f"Success Rate: {profile.get('success_rate', 0):.2%}")
        print(f"Avg Session Duration: {profile.get('avg_session_duration', 0):.1f} minutes")

def main():
    profiler = UserProfiler()
    
    print("Loading authentication logs...")
    df = profiler.load_data("data/sample_logs.json")
    
    print(f"Loaded {len(df)} authentication events for {df['user_id'].nunique()} users")
    
    print("Creating user behavioral profiles...")
    profiles = profiler.create_user_profiles(df)
    
    print(f"Created profiles for {len(profiles)} users")
    
    # Save profiles
    profiler.save_profiles("data/user_profiles.json")
    print("User profiles saved to data/user_profiles.json")
    
    # Show sample profiles
    for user_id in list(profiles.keys())[:3]:
        profiler.print_user_summary(user_id)

if __name__ == "__main__":
    main()