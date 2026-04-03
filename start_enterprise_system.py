#!/usr/bin/env python3
"""
Enterprise Identity Anomaly Detection System - Startup Script
Comprehensive system launcher with health checks and monitoring
"""

import os
import sys
import time
import subprocess
import threading
import signal
import json
from datetime import datetime
import requests
import psutil

class SystemLauncher:
    def __init__(self):
        self.processes = {}
        self.running = True
        self.health_checks = {}
        
    def print_banner(self):
        """Print system banner"""
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    🛡️  ENTERPRISE IDENTITY ANOMALY DETECTION SYSTEM                         ║
║                                                                              ║
║    🚀 Complete Production-Ready Security Platform                           ║
║    🧠 Advanced ML-Powered Threat Detection                                  ║
║    ⚡ Real-time Processing & Alerting                                       ║
║    🌐 Modern React Dashboard                                                ║
║    🔌 Enterprise Integrations (SIEM, SOAR, ITSM)                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
        print(f"🕐 System Starting: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

    def check_dependencies(self):
        """Check system dependencies"""
        print("🔍 Checking system dependencies...")
        
        dependencies = {
            'python': {'cmd': 'python --version', 'required': True},
            'node': {'cmd': 'node --version', 'required': True},
            'npm': {'cmd': 'npm --version', 'required': True},
            'docker': {'cmd': 'docker --version', 'required': False},
            'redis': {'cmd': 'redis-server --version', 'required': False},
        }
        
        missing_required = []
        
        for dep, config in dependencies.items():
            try:
                result = subprocess.run(
                    config['cmd'].split(), 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                if result.returncode == 0:
                    version = result.stdout.strip().split('\n')[0]
                    print(f"  ✅ {dep}: {version}")
                else:
                    if config['required']:
                        missing_required.append(dep)
                    print(f"  ❌ {dep}: Not found")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                if config['required']:
                    missing_required.append(dep)
                print(f"  ❌ {dep}: Not found")
        
        if missing_required:
            print(f"\n❌ Missing required dependencies: {', '.join(missing_required)}")
            print("Please install missing dependencies and try again.")
            return False
        
        print("✅ All required dependencies found")
        return True

    def setup_environment(self):
        """Setup environment and directories"""
        print("\n🔧 Setting up environment...")
        
        # Create necessary directories
        directories = [
            'data', 'logs', 'models', 'reports', 'backups',
            'monitoring/grafana/dashboards',
            'monitoring/grafana/datasources',
            'monitoring/prometheus'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"  📁 Created directory: {directory}")
        
        # Create environment files if they don't exist
        env_files = {
            '.env': """
# Environment Configuration
FLASK_ENV=development
REDIS_URL=redis://localhost:6379
DATABASE_URL=sqlite:///data/identity_anomaly.db
SECRET_KEY=your-secret-key-here
API_PORT=8000
FRONTEND_PORT=3000
            """.strip(),
            'frontend/.env': """
# Frontend Environment
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
            """.strip()
        }
        
        for file_path, content in env_files.items():
            if not os.path.exists(file_path):
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w') as f:
                    f.write(content)
                print(f"  📄 Created environment file: {file_path}")
        
        print("✅ Environment setup completed")

    def install_dependencies(self):
        """Install Python and Node.js dependencies"""
        print("\n📦 Installing dependencies...")
        
        # Install Python dependencies
        print("  🐍 Installing Python dependencies...")
        try:
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
            ], check=True, capture_output=True)
            print("  ✅ Python dependencies installed")
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Failed to install Python dependencies: {e}")
            return False
        
        # Install Node.js dependencies
        if os.path.exists('frontend/package.json'):
            print("  📦 Installing Node.js dependencies...")
            try:
                subprocess.run([
                    'npm', 'install'
                ], cwd='frontend', check=True, capture_output=True)
                print("  ✅ Node.js dependencies installed")
            except subprocess.CalledProcessError as e:
                print(f"  ❌ Failed to install Node.js dependencies: {e}")
                return False
        
        return True

    def start_backend_services(self):
        """Start backend services"""
        print("\n🚀 Starting backend services...")
        
        # Start API Server
        print("  🌐 Starting API Server...")
        api_process = subprocess.Popen([
            sys.executable, 'src/api_server.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        self.processes['api_server'] = api_process
        print(f"  ✅ API Server started (PID: {api_process.pid})")
        
        # Wait for API server to be ready
        self.wait_for_service('http://localhost:8000/api/health', 'API Server')
        
        return True

    def start_frontend(self):
        """Start frontend application"""
        print("\n🎨 Starting frontend application...")
        
        if not os.path.exists('frontend/package.json'):
            print("  ⚠️  Frontend not found, skipping...")
            return True
        
        try:
            # Start React development server
            frontend_process = subprocess.Popen([
                'npm', 'start'
            ], cwd='frontend', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.processes['frontend'] = frontend_process
            print(f"  ✅ Frontend started (PID: {frontend_process.pid})")
            
            # Wait for frontend to be ready
            self.wait_for_service('http://localhost:3000', 'Frontend')
            
            return True
            
        except Exception as e:
            print(f"  ❌ Failed to start frontend: {e}")
            return False

    def wait_for_service(self, url, service_name, timeout=60):
        """Wait for a service to be ready"""
        print(f"  ⏳ Waiting for {service_name} to be ready...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"  ✅ {service_name} is ready")
                    return True
            except requests.exceptions.RequestException:
                pass
            
            time.sleep(2)
        
        print(f"  ⚠️  {service_name} not ready after {timeout}s")
        return False

    def start_monitoring(self):
        """Start monitoring and health checks"""
        print("\n📊 Starting monitoring...")
        
        def health_check_loop():
            while self.running:
                try:
                    # Check API Server
                    try:
                        response = requests.get('http://localhost:8000/api/health', timeout=5)
                        self.health_checks['api_server'] = response.status_code == 200
                    except:
                        self.health_checks['api_server'] = False
                    
                    # Check Frontend
                    try:
                        response = requests.get('http://localhost:3000', timeout=5)
                        self.health_checks['frontend'] = response.status_code == 200
                    except:
                        self.health_checks['frontend'] = False
                    
                    # Check processes
                    for name, process in self.processes.items():
                        if process.poll() is None:
                            self.health_checks[f'{name}_process'] = True
                        else:
                            self.health_checks[f'{name}_process'] = False
                            print(f"  ⚠️  Process {name} has stopped")
                    
                except Exception as e:
                    print(f"  ❌ Health check error: {e}")
                
                time.sleep(10)
        
        health_thread = threading.Thread(target=health_check_loop, daemon=True)
        health_thread.start()
        
        print("  ✅ Health monitoring started")

    def print_system_status(self):
        """Print system status and URLs"""
        print("\n" + "=" * 80)
        print("🎉 SYSTEM STARTUP COMPLETED")
        print("=" * 80)
        
        services = [
            {
                'name': '🌐 API Server',
                'url': 'http://localhost:8000',
                'description': 'RESTful API and WebSocket server'
            },
            {
                'name': '🎨 Frontend Dashboard',
                'url': 'http://localhost:3000',
                'description': 'React-based security operations center'
            },
            {
                'name': '📊 API Health Check',
                'url': 'http://localhost:8000/api/health',
                'description': 'System health and metrics'
            },
            {
                'name': '🔍 API Documentation',
                'url': 'http://localhost:8000/api/docs',
                'description': 'Interactive API documentation'
            }
        ]
        
        print("\n📍 Available Services:")
        for service in services:
            print(f"  {service['name']}: {service['url']}")
            print(f"     {service['description']}")
        
        print("\n🔧 System Features:")
        features = [
            "✅ Advanced ML-powered anomaly detection",
            "✅ Real-time event processing and alerting",
            "✅ Interactive security dashboard",
            "✅ User behavior analytics",
            "✅ Threat hunting capabilities",
            "✅ Enterprise integrations (SIEM, SOAR, ITSM)",
            "✅ Comprehensive reporting system",
            "✅ WebSocket real-time updates",
            "✅ RESTful API with authentication",
            "✅ Scalable microservices architecture"
        ]
        
        for feature in features:
            print(f"  {feature}")
        
        print("\n📚 Quick Start Guide:")
        print("  1. Open http://localhost:3000 in your browser")
        print("  2. The system will auto-authenticate for demo purposes")
        print("  3. Explore the dashboard and security features")
        print("  4. Use 'Simulate Attack' button to test detection")
        print("  5. Check alerts and user analytics")
        
        print("\n🛑 To stop the system:")
        print("  Press Ctrl+C or run: python stop_system.py")
        
        print("\n" + "=" * 80)

    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n🛑 Received signal {signum}, shutting down...")
        self.shutdown()

    def shutdown(self):
        """Shutdown all services"""
        print("\n🔄 Shutting down services...")
        self.running = False
        
        for name, process in self.processes.items():
            if process.poll() is None:
                print(f"  🛑 Stopping {name}...")
                process.terminate()
                
                # Wait for graceful shutdown
                try:
                    process.wait(timeout=10)
                    print(f"  ✅ {name} stopped gracefully")
                except subprocess.TimeoutExpired:
                    print(f"  ⚠️  Force killing {name}...")
                    process.kill()
        
        print("✅ All services stopped")
        sys.exit(0)

    def run(self):
        """Main execution method"""
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        try:
            # System startup sequence
            self.print_banner()
            
            if not self.check_dependencies():
                return False
            
            self.setup_environment()
            
            if not self.install_dependencies():
                return False
            
            if not self.start_backend_services():
                return False
            
            if not self.start_frontend():
                return False
            
            self.start_monitoring()
            self.print_system_status()
            
            # Keep the system running
            print("\n🔄 System is running... Press Ctrl+C to stop")
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Keyboard interrupt received")
            self.shutdown()
        except Exception as e:
            print(f"\n❌ System error: {e}")
            self.shutdown()
            return False
        
        return True

def main():
    """Main entry point"""
    launcher = SystemLauncher()
    success = launcher.run()
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())