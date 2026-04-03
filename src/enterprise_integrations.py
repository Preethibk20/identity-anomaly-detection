#!/usr/bin/env python3
"""
Enterprise Integrations - SIEM, SOAR, and API integrations
"""

import asyncio
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
import logging
from dataclasses import dataclass, asdict
import xml.etree.ElementTree as ET
from urllib.parse import urljoin
import base64
import hmac
import hashlib

logger = logging.getLogger(__name__)

@dataclass
class IntegrationConfig:
    name: str
    type: str
    endpoint: str
    credentials: Dict[str, str]
    enabled: bool = True
    timeout: int = 30
    retry_count: int = 3

class BaseIntegration(ABC):
    """Base class for all integrations"""
    
    def __init__(self, config: IntegrationConfig):
        self.config = config
        self.session = requests.Session()
        self.session.timeout = config.timeout
    
    @abstractmethod
    async def send_alert(self, alert_data: Dict) -> bool:
        """Send alert to external system"""
        pass
    
    @abstractmethod
    async def test_connection(self) -> bool:
        """Test connection to external system"""
        pass
    
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make HTTP request with retry logic"""
        for attempt in range(self.config.retry_count):
            try:
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request attempt {attempt + 1} failed: {e}")
                if attempt == self.config.retry_count - 1:
                    raise
        
        raise Exception("All retry attempts failed")

class SplunkIntegration(BaseIntegration):
    """Splunk SIEM Integration"""
    
    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.hec_token = config.credentials.get('hec_token')
        self.index = config.credentials.get('index', 'security')
    
    async def send_alert(self, alert_data: Dict) -> bool:
        """Send alert to Splunk via HTTP Event Collector"""
        try:
            # Format for Splunk HEC
            splunk_event = {
                "time": int(datetime.now().timestamp()),
                "index": self.index,
                "sourcetype": "identity_anomaly_alert",
                "source": "identity_anomaly_detection",
                "event": {
                    "alert_id": alert_data.get('id'),
                    "severity": alert_data.get('severity'),
                    "risk_score": alert_data.get('risk_score'),
                    "user_id": alert_data.get('user_id'),
                    "title": alert_data.get('title'),
                    "description": alert_data.get('description'),
                    "timestamp": alert_data.get('timestamp'),
                    "source_event": alert_data.get('source_event', {}),
                    "tags": alert_data.get('tags', [])
                }
            }
            
            headers = {
                'Authorization': f'Splunk {self.hec_token}',
                'Content-Type': 'application/json'
            }
            
            url = urljoin(self.config.endpoint, '/services/collector')
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self._make_request('POST', url, json=splunk_event, headers=headers)
            )
            
            logger.info(f"Alert sent to Splunk: {alert_data.get('id')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send alert to Splunk: {e}")
            return False
    
    async def test_connection(self) -> bool:
        """Test Splunk connection"""
        try:
            headers = {
                'Authorization': f'Splunk {self.hec_token}',
                'Content-Type': 'application/json'
            }
            
            test_event = {
                "time": int(datetime.now().timestamp()),
                "event": {"test": "connection"}
            }
            
            url = urljoin(self.config.endpoint, '/services/collector')
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self._make_request('POST', url, json=test_event, headers=headers)
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Splunk connection test failed: {e}")
            return False

class QRadarIntegration(BaseIntegration):
    """IBM QRadar SIEM Integration"""
    
    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.api_token = config.credentials.get('api_token')
        self.session.headers.update({
            'SEC': self.api_token,
            'Content-Type': 'application/json',
            'Version': '12.0'
        })
    
    async def send_alert(self, alert_data: Dict) -> bool:
        """Send alert to QRadar as custom event"""
        try:
            # Format for QRadar custom event
            qradar_event = {
                "events": [{
                    "qid": 55500001,  # Custom QID for identity anomalies
                    "message": f"Identity Anomaly: {alert_data.get('title')}",
                    "severity": self._map_severity_to_qradar(alert_data.get('severity')),
                    "properties": [
                        {"name": "AlertID", "value": alert_data.get('id')},
                        {"name": "UserID", "value": alert_data.get('user_id')},
                        {"name": "RiskScore", "value": str(alert_data.get('risk_score'))},
                        {"name": "Description", "value": alert_data.get('description')},
                        {"name": "Tags", "value": ",".join(alert_data.get('tags', []))}
                    ]
                }]
            }
            
            url = urljoin(self.config.endpoint, '/api/siem/events')
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self._make_request('POST', url, json=qradar_event)
            )
            
            logger.info(f"Alert sent to QRadar: {alert_data.get('id')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send alert to QRadar: {e}")
            return False
    
    def _map_severity_to_qradar(self, severity: str) -> int:
        """Map severity to QRadar severity levels"""
        mapping = {
            'low': 3,
            'medium': 5,
            'high': 7,
            'critical': 9
        }
        return mapping.get(severity.lower(), 5)
    
    async def test_connection(self) -> bool:
        """Test QRadar connection"""
        try:
            url = urljoin(self.config.endpoint, '/api/system/about')
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self._make_request('GET', url)
            )
            
            return True
            
        except Exception as e:
            logger.error(f"QRadar connection test failed: {e}")
            return False

class SentinelIntegration(BaseIntegration):
    """Microsoft Sentinel Integration"""
    
    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.workspace_id = config.credentials.get('workspace_id')
        self.shared_key = config.credentials.get('shared_key')
        self.log_type = 'IdentityAnomalyAlert'
    
    async def send_alert(self, alert_data: Dict) -> bool:
        """Send alert to Sentinel via Data Collector API"""
        try:
            # Format for Sentinel
            sentinel_data = [{
                "AlertId": alert_data.get('id'),
                "Severity": alert_data.get('severity'),
                "RiskScore": alert_data.get('risk_score'),
                "UserId": alert_data.get('user_id'),
                "Title": alert_data.get('title'),
                "Description": alert_data.get('description'),
                "Timestamp": alert_data.get('timestamp'),
                "SourceEvent": json.dumps(alert_data.get('source_event', {})),
                "Tags": ",".join(alert_data.get('tags', []))
            }]
            
            json_data = json.dumps(sentinel_data)
            
            # Build signature for authentication
            date_string = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
            string_to_hash = f"POST\n{len(json_data)}\napplication/json\nx-ms-date:{date_string}\n/api/logs"
            bytes_to_hash = bytes(string_to_hash, 'UTF-8')
            decoded_key = base64.b64decode(self.shared_key)
            encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()).decode()
            authorization = f"SharedKey {self.workspace_id}:{encoded_hash}"
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': authorization,
                'Log-Type': self.log_type,
                'x-ms-date': date_string
            }
            
            url = f"https://{self.workspace_id}.ods.opinsights.azure.com/api/logs?api-version=2016-04-01"
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self._make_request('POST', url, data=json_data, headers=headers)
            )
            
            logger.info(f"Alert sent to Sentinel: {alert_data.get('id')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send alert to Sentinel: {e}")
            return False
    
    async def test_connection(self) -> bool:
        """Test Sentinel connection"""
        try:
            # Send a test event
            test_data = [{
                "TestEvent": "Connection Test",
                "Timestamp": datetime.utcnow().isoformat()
            }]
            
            json_data = json.dumps(test_data)
            
            # Build signature
            date_string = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
            string_to_hash = f"POST\n{len(json_data)}\napplication/json\nx-ms-date:{date_string}\n/api/logs"
            bytes_to_hash = bytes(string_to_hash, 'UTF-8')
            decoded_key = base64.b64decode(self.shared_key)
            encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()).decode()
            authorization = f"SharedKey {self.workspace_id}:{encoded_hash}"
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': authorization,
                'Log-Type': 'TestConnection',
                'x-ms-date': date_string
            }
            
            url = f"https://{self.workspace_id}.ods.opinsights.azure.com/api/logs?api-version=2016-04-01"
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self._make_request('POST', url, data=json_data, headers=headers)
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Sentinel connection test failed: {e}")
            return False
class ServiceNowIntegration(BaseIntegration):
    """ServiceNow ITSM Integration"""
    
    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        username = config.credentials.get('username')
        password = config.credentials.get('password')
        self.session.auth = (username, password)
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    async def send_alert(self, alert_data: Dict) -> bool:
        """Create ServiceNow incident from alert"""
        try:
            # Map severity to ServiceNow impact/urgency
            impact, urgency = self._map_severity_to_servicenow(alert_data.get('severity'))
            
            incident_data = {
                "short_description": alert_data.get('title'),
                "description": f"{alert_data.get('description')}\n\nAlert ID: {alert_data.get('id')}\nRisk Score: {alert_data.get('risk_score')}\nUser: {alert_data.get('user_id')}",
                "category": "Security",
                "subcategory": "Identity Management",
                "impact": impact,
                "urgency": urgency,
                "caller_id": "security.system",
                "assignment_group": "Security Operations",
                "work_notes": f"Automated incident created from identity anomaly detection system. Tags: {', '.join(alert_data.get('tags', []))}"
            }
            
            url = urljoin(self.config.endpoint, '/api/now/table/incident')
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self._make_request('POST', url, json=incident_data)
            )
            
            incident_number = response.json().get('result', {}).get('number')
            logger.info(f"ServiceNow incident created: {incident_number} for alert {alert_data.get('id')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create ServiceNow incident: {e}")
            return False
    
    def _map_severity_to_servicenow(self, severity: str) -> tuple:
        """Map severity to ServiceNow impact/urgency"""
        mapping = {
            'critical': ('1', '1'),  # High impact, High urgency
            'high': ('2', '2'),      # Medium impact, Medium urgency
            'medium': ('3', '3'),    # Low impact, Low urgency
            'low': ('3', '3')        # Low impact, Low urgency
        }
        return mapping.get(severity.lower(), ('3', '3'))
    
    async def test_connection(self) -> bool:
        """Test ServiceNow connection"""
        try:
            url = urljoin(self.config.endpoint, '/api/now/table/sys_user?sysparm_limit=1')
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self._make_request('GET', url)
            )
            
            return True
            
        except Exception as e:
            logger.error(f"ServiceNow connection test failed: {e}")
            return False

class SlackIntegration(BaseIntegration):
    """Slack Integration for notifications"""
    
    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.webhook_url = config.credentials.get('webhook_url')
        self.channel = config.credentials.get('channel', '#security-alerts')
    
    async def send_alert(self, alert_data: Dict) -> bool:
        """Send alert to Slack channel"""
        try:
            # Format Slack message
            severity_emoji = {
                'critical': '🚨',
                'high': '⚠️',
                'medium': '🟡',
                'low': '🟢'
            }
            
            emoji = severity_emoji.get(alert_data.get('severity', 'medium'), '🔍')
            
            slack_message = {
                "channel": self.channel,
                "username": "Identity Anomaly Detection",
                "icon_emoji": ":shield:",
                "attachments": [{
                    "color": self._get_color_for_severity(alert_data.get('severity')),
                    "title": f"{emoji} {alert_data.get('title')}",
                    "text": alert_data.get('description'),
                    "fields": [
                        {
                            "title": "User",
                            "value": alert_data.get('user_id'),
                            "short": True
                        },
                        {
                            "title": "Risk Score",
                            "value": f"{alert_data.get('risk_score')}/100",
                            "short": True
                        },
                        {
                            "title": "Severity",
                            "value": alert_data.get('severity', 'Unknown').upper(),
                            "short": True
                        },
                        {
                            "title": "Alert ID",
                            "value": alert_data.get('id'),
                            "short": True
                        }
                    ],
                    "footer": "Identity Anomaly Detection System",
                    "ts": int(datetime.now().timestamp())
                }]
            }
            
            if alert_data.get('tags'):
                slack_message["attachments"][0]["fields"].append({
                    "title": "Tags",
                    "value": ", ".join(alert_data.get('tags')),
                    "short": False
                })
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self._make_request('POST', self.webhook_url, json=slack_message)
            )
            
            logger.info(f"Alert sent to Slack: {alert_data.get('id')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send alert to Slack: {e}")
            return False
    
    def _get_color_for_severity(self, severity: str) -> str:
        """Get color code for severity"""
        colors = {
            'critical': '#FF0000',
            'high': '#FF8C00',
            'medium': '#FFD700',
            'low': '#32CD32'
        }
        return colors.get(severity.lower(), '#808080')
    
    async def test_connection(self) -> bool:
        """Test Slack connection"""
        try:
            test_message = {
                "channel": self.channel,
                "text": "🧪 Test message from Identity Anomaly Detection System",
                "username": "Identity Anomaly Detection"
            }
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self._make_request('POST', self.webhook_url, json=test_message)
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Slack connection test failed: {e}")
            return False

class IntegrationManager:
    """Manage all enterprise integrations"""
    
    def __init__(self):
        self.integrations: Dict[str, BaseIntegration] = {}
        self.integration_classes = {
            'splunk': SplunkIntegration,
            'qradar': QRadarIntegration,
            'sentinel': SentinelIntegration,
            'servicenow': ServiceNowIntegration,
            'slack': SlackIntegration
        }
    
    def add_integration(self, config: IntegrationConfig):
        """Add an integration"""
        integration_class = self.integration_classes.get(config.type.lower())
        if not integration_class:
            raise ValueError(f"Unknown integration type: {config.type}")
        
        integration = integration_class(config)
        self.integrations[config.name] = integration
        logger.info(f"Added integration: {config.name} ({config.type})")
    
    def remove_integration(self, name: str):
        """Remove an integration"""
        if name in self.integrations:
            del self.integrations[name]
            logger.info(f"Removed integration: {name}")
    
    async def send_alert_to_all(self, alert_data: Dict) -> Dict[str, bool]:
        """Send alert to all enabled integrations"""
        results = {}
        
        tasks = []
        for name, integration in self.integrations.items():
            if integration.config.enabled:
                task = asyncio.create_task(
                    self._send_alert_safe(name, integration, alert_data)
                )
                tasks.append(task)
        
        if tasks:
            task_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for i, (name, _) in enumerate(self.integrations.items()):
                if i < len(task_results):
                    results[name] = task_results[i] if not isinstance(task_results[i], Exception) else False
        
        return results
    
    async def _send_alert_safe(self, name: str, integration: BaseIntegration, alert_data: Dict) -> bool:
        """Send alert with error handling"""
        try:
            return await integration.send_alert(alert_data)
        except Exception as e:
            logger.error(f"Integration {name} failed: {e}")
            return False
    
    async def test_all_connections(self) -> Dict[str, bool]:
        """Test all integration connections"""
        results = {}
        
        for name, integration in self.integrations.items():
            try:
                results[name] = await integration.test_connection()
            except Exception as e:
                logger.error(f"Connection test failed for {name}: {e}")
                results[name] = False
        
        return results
    
    def get_integration_status(self) -> Dict[str, Dict]:
        """Get status of all integrations"""
        status = {}
        
        for name, integration in self.integrations.items():
            status[name] = {
                'type': integration.config.type,
                'enabled': integration.config.enabled,
                'endpoint': integration.config.endpoint,
                'timeout': integration.config.timeout
            }
        
        return status

# Global integration manager
integration_manager = IntegrationManager()

def setup_default_integrations():
    """Setup default integrations with sample configurations"""
    
    # Splunk integration
    splunk_config = IntegrationConfig(
        name="splunk_prod",
        type="splunk",
        endpoint="https://splunk.company.com:8088",
        credentials={
            "hec_token": "your-hec-token-here",
            "index": "security"
        }
    )
    
    # QRadar integration
    qradar_config = IntegrationConfig(
        name="qradar_prod",
        type="qradar",
        endpoint="https://qradar.company.com",
        credentials={
            "api_token": "your-api-token-here"
        }
    )
    
    # Sentinel integration
    sentinel_config = IntegrationConfig(
        name="sentinel_prod",
        type="sentinel",
        endpoint="https://your-workspace.ods.opinsights.azure.com",
        credentials={
            "workspace_id": "your-workspace-id",
            "shared_key": "your-shared-key"
        }
    )
    
    # ServiceNow integration
    servicenow_config = IntegrationConfig(
        name="servicenow_prod",
        type="servicenow",
        endpoint="https://your-instance.service-now.com",
        credentials={
            "username": "integration_user",
            "password": "your-password"
        }
    )
    
    # Slack integration
    slack_config = IntegrationConfig(
        name="slack_security",
        type="slack",
        endpoint="https://hooks.slack.com/services/...",
        credentials={
            "webhook_url": "https://hooks.slack.com/services/your/webhook/url",
            "channel": "#security-alerts"
        }
    )
    
    # Add integrations (disabled by default for demo)
    for config in [splunk_config, qradar_config, sentinel_config, servicenow_config, slack_config]:
        config.enabled = False  # Disable for demo
        try:
            integration_manager.add_integration(config)
        except Exception as e:
            logger.warning(f"Failed to add integration {config.name}: {e}")

async def main():
    """Test enterprise integrations"""
    print("🔌 Enterprise Integrations - Testing")
    print("=" * 50)
    
    # Setup integrations
    setup_default_integrations()
    
    # Get integration status
    status = integration_manager.get_integration_status()
    print(f"\nConfigured integrations: {len(status)}")
    for name, info in status.items():
        print(f"  {name}: {info['type']} ({'enabled' if info['enabled'] else 'disabled'})")
    
    # Test sample alert
    sample_alert = {
        'id': 'test-alert-123',
        'severity': 'high',
        'risk_score': 85,
        'user_id': 'john.doe',
        'title': 'Suspicious Login from Moscow',
        'description': 'User logged in from unusual location at 3 AM',
        'timestamp': datetime.now().isoformat(),
        'source_event': {
            'location': 'Moscow',
            'time': '03:00:00',
            'device': 'unknown'
        },
        'tags': ['account_compromise', 'unusual_location']
    }
    
    # Send to all integrations (will be skipped since disabled)
    results = await integration_manager.send_alert_to_all(sample_alert)
    print(f"\nAlert sending results: {results}")
    
    print("\n✅ Enterprise integrations testing completed!")

if __name__ == "__main__":
    asyncio.run(main())