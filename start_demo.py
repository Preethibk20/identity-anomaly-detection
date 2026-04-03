#!/usr/bin/env python3
"""
Identity Anomaly Detection System - Demo Launcher

This script starts the main demonstration system.
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    try:
        import flask
        import pandas
        import sklearn
        import numpy
        print("✓ All required packages are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing required package: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def main():
    """Main function to start the demo"""
    print("=" * 60)
    print("Identity Anomaly Detection System")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        return
    
    print("\nStarting system components...")
    
    # Check if data directory exists
    data_dir = Path("data")
    if not data_dir.exists():
        print("Creating data directory...")
        data_dir.mkdir()
    
    try:
        print("Starting demo server...")
        print("Demo will be available at: http://localhost:5002")
        print("\nPress Ctrl+C to stop the server")
        print("=" * 60)
        
        # Start the demo server
        subprocess.run([sys.executable, "enhanced_intelligence_demo.py"])
        
    except KeyboardInterrupt:
        print("\nShutting down demo server...")
        print("Thank you for using the Identity Anomaly Detection System!")
    except Exception as e:
        print(f"Error starting demo: {e}")
        print("Please check the installation and try again.")

if __name__ == "__main__":
    main()