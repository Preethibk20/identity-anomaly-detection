import json
import random
from datetime import datetime, timedelta
import pandas as pd

class AuthLogGenerator:
    def __init__(self):
        self.users = [
            "john.doe", "jane.smith", "mike.wilson", "sarah.johnson", 
            "david.brown", "lisa.davis", "tom.miller", "anna.garcia"
        ]
        
        self.locations = [
            "New York", "London", "Tokyo", "Sydney", "Toronto", 
            "Berlin", "Paris", "Singapore", "Mumbai", "São Paulo"
        ]
        
        self.devices = ["laptop", "desktop", "mobile", "tablet"]
        self.resources = [
            "email", "file_server", "database", "crm_system", 
            "hr_portal", "finance_app", "admin_panel", "reports"
        ]
        
        # Define normal patterns for each user
        self.user_patterns = {
            "john.doe": {"work_hours": (9, 17), "location": "New York", "device": "laptop"},
            "jane.smith": {"work_hours": (8, 16), "location": "London", "device": "desktop"},
            "mike.wilson": {"work_hours": (10, 18), "location": "Toronto", "device": "laptop"},
            "sarah.johnson": {"work_hours": (9, 17), "location": "Sydney", "device": "mobile"},
            "david.brown": {"work_hours": (8, 16), "location": "Berlin", "device": "desktop"},
            "lisa.davis": {"work_hours": (9, 17), "location": "New York", "device": "laptop"},
            "tom.miller": {"work_hours": (10, 18), "location": "Paris", "device": "tablet"},
            "anna.garcia": {"work_hours": (8, 16), "location": "Singapore", "device": "laptop"}
        }
    
    def generate_normal_activity(self, user, date, num_events=5):
        """Generate normal user activity for a given date"""
        events = []
        pattern = self.user_patterns[user]
        
        # Generate login events during work hours
        for i in range(num_events):
            # Normal work hours with some variation
            hour = random.randint(pattern["work_hours"][0], pattern["work_hours"][1])
            minute = random.randint(0, 59)
            
            timestamp = date.replace(hour=hour, minute=minute, second=random.randint(0, 59))
            
            event = {
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "user_id": user,
                "action": random.choice(["login", "access_resource", "logout"]),
                "location": pattern["location"],
                "ip_address": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "device": pattern["device"],
                "resource": random.choice(self.resources[:4]),  # Normal resources
                "success": True,
                "session_duration": random.randint(30, 480)  # 30 min to 8 hours
            }
            events.append(event)
        
        return events
    
    def generate_suspicious_activity(self, user, date, scenario="compromised"):
        """Generate suspicious activity based on different scenarios"""
        events = []
        
        if scenario == "compromised":
            # Compromised account: unusual location, off-hours access
            suspicious_times = [2, 3, 23, 1]  # Late night/early morning
            for hour in suspicious_times:
                timestamp = date.replace(hour=hour, minute=random.randint(0, 59))
                
                event = {
                    "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "user_id": user,
                    "action": "login",
                    "location": random.choice(["Moscow", "Beijing", "Unknown"]),  # Unusual location
                    "ip_address": f"10.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                    "device": "unknown_device",
                    "resource": random.choice(self.resources),
                    "success": True,
                    "session_duration": random.randint(120, 300)  # Longer sessions
                }
                events.append(event)
        
        elif scenario == "insider_threat":
            # Insider threat: accessing sensitive resources, weekend work
            if date.weekday() >= 5:  # Weekend
                for i in range(3):
                    hour = random.randint(10, 22)
                    timestamp = date.replace(hour=hour, minute=random.randint(0, 59))
                    
                    event = {
                        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                        "user_id": user,
                        "action": "access_resource",
                        "location": self.user_patterns[user]["location"],
                        "ip_address": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                        "device": self.user_patterns[user]["device"],
                        "resource": random.choice(["admin_panel", "database", "finance_app"]),  # Sensitive resources
                        "success": True,
                        "session_duration": random.randint(180, 600)  # Very long sessions
                    }
                    events.append(event)
        
        elif scenario == "failed_attempts":
            # Multiple failed login attempts
            for i in range(8):
                hour = random.randint(8, 18)
                timestamp = date.replace(hour=hour, minute=random.randint(0, 59))
                
                event = {
                    "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "user_id": user,
                    "action": "login",
                    "location": self.user_patterns[user]["location"],
                    "ip_address": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                    "device": self.user_patterns[user]["device"],
                    "resource": "login_portal",
                    "success": False,  # Failed attempts
                    "session_duration": 0
                }
                events.append(event)
        
        return events
    
    def generate_dataset(self, days=30):
        """Generate complete dataset with normal and suspicious activities"""
        all_events = []
        start_date = datetime.now() - timedelta(days=days)
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            
            # Generate normal activity for all users
            for user in self.users:
                if current_date.weekday() < 5:  # Weekdays only for normal activity
                    events = self.generate_normal_activity(user, current_date)
                    all_events.extend(events)
            
            # Add some suspicious activities
            if day > 20:  # Add suspicious activity in recent days
                if random.random() < 0.3:  # 30% chance of suspicious activity
                    suspicious_user = random.choice(self.users[:3])  # Focus on first 3 users
                    scenario = random.choice(["compromised", "insider_threat", "failed_attempts"])
                    suspicious_events = self.generate_suspicious_activity(suspicious_user, current_date, scenario)
                    all_events.extend(suspicious_events)
        
        return sorted(all_events, key=lambda x: x["timestamp"])

def main():
    generator = AuthLogGenerator()
    
    print("Generating authentication logs...")
    events = generator.generate_dataset(days=30)
    
    # Save to JSON file
    with open("data/sample_logs.json", "w") as f:
        json.dump(events, f, indent=2)
    
    # Also save as CSV for easier analysis
    df = pd.DataFrame(events)
    df.to_csv("data/sample_logs.csv", index=False)
    
    print(f"Generated {len(events)} authentication events")
    print("Files saved:")
    print("- data/sample_logs.json")
    print("- data/sample_logs.csv")
    
    # Show sample data
    print("\nSample events:")
    for event in events[:5]:
        print(f"  {event['timestamp']} - {event['user_id']} - {event['action']} - {event['location']}")

if __name__ == "__main__":
    main()