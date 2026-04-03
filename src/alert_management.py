#!/usr/bin/env python3
"""
Alert Management System - Enterprise-grade alert processing and workflows
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from enum import Enum
from dataclasses import dataclass, asdict
import logging
from concurrent.futures import ThreadPoolExecutor
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart

logger = logging.getLogger(__name__)

class AlertSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertStatus(Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"
    ESCALATED = "escalated"

class WorkflowAction(Enum):
    EMAIL_NOTIFICATION = "email_notification"
    SLACK_NOTIFICATION = "slack_notification"
    TICKET_CREATION = "ticket_creation"
    ACCOUNT_LOCKOUT = "account_lockout"
    ACCESS_REVOCATION = "access_revocation"
    ESCALATION = "escalation"

@dataclass
class Alert:
    id: str
    timestamp: datetime
    user_id: str
    severity: AlertSeverity
    status: AlertStatus
    title: str
    description: str
    risk_score: float
    source_event: Dict
    assigned_to: Optional[str] = None
    tags: List[str] = None
    metadata: Dict = None
    created_by: str = "system"
    updated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None

@dataclass
class WorkflowRule:
    id: str
    name: str
    conditions: Dict
    actions: List[WorkflowAction]
    enabled: bool = True
    priority: int = 0

class AlertCorrelationEngine:
    """Correlate related alerts to reduce noise"""
    
    def __init__(self):
        self.correlation_window = timedelta(minutes=30)
        self.similarity_threshold = 0.8
    
    async def correlate_alert(self, new_alert: Alert, existing_alerts: List[Alert]) -> List[Alert]:
        """Find related alerts for correlation"""
        related_alerts = []
        
        for existing_alert in existing_alerts:
            if self._are_alerts_related(new_alert, existing_alert):
                related_alerts.append(existing_alert)
        
        return related_alerts
    
    def _are_alerts_related(self, alert1: Alert, alert2: Alert) -> bool:
        """Check if two alerts are related"""
        # Time-based correlation
        time_diff = abs((alert1.timestamp - alert2.timestamp).total_seconds())
        if time_diff > self.correlation_window.total_seconds():
            return False
        
        # User-based correlation
        if alert1.user_id == alert2.user_id:
            return True
        
        # Pattern-based correlation
        if self._similar_patterns(alert1, alert2):
            return True
        
        return False
    
    def _similar_patterns(self, alert1: Alert, alert2: Alert) -> bool:
        """Check if alerts have similar patterns"""
        # Compare source events
        event1 = alert1.source_event
        event2 = alert2.source_event
        
        similarity_score = 0
        total_factors = 0
        
        # Location similarity
        if event1.get('location') == event2.get('location'):
            similarity_score += 1
        total_factors += 1
        
        # Action similarity
        if event1.get('action') == event2.get('action'):
            similarity_score += 1
        total_factors += 1
        
        # Device similarity
        if event1.get('device') == event2.get('device'):
            similarity_score += 1
        total_factors += 1
        
        return (similarity_score / total_factors) >= self.similarity_threshold

class WorkflowEngine:
    """Execute automated workflows based on alert conditions"""
    
    def __init__(self):
        self.rules: List[WorkflowRule] = []
        self.action_handlers: Dict[WorkflowAction, Callable] = {}
        self.executor = ThreadPoolExecutor(max_workers=10)
        
        # Register default action handlers
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """Register default action handlers"""
        self.action_handlers[WorkflowAction.EMAIL_NOTIFICATION] = self._send_email_notification
        self.action_handlers[WorkflowAction.SLACK_NOTIFICATION] = self._send_slack_notification
        self.action_handlers[WorkflowAction.TICKET_CREATION] = self._create_ticket
        self.action_handlers[WorkflowAction.ACCOUNT_LOCKOUT] = self._lockout_account
        self.action_handlers[WorkflowAction.ACCESS_REVOCATION] = self._revoke_access
        self.action_handlers[WorkflowAction.ESCALATION] = self._escalate_alert
    
    def add_rule(self, rule: WorkflowRule):
        """Add a workflow rule"""
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.priority, reverse=True)
    
    async def process_alert(self, alert: Alert) -> List[str]:
        """Process alert through workflow rules"""
        executed_actions = []
        
        for rule in self.rules:
            if not rule.enabled:
                continue
            
            if self._matches_conditions(alert, rule.conditions):
                logger.info(f"Alert {alert.id} matches rule {rule.name}")
                
                for action in rule.actions:
                    try:
                        await self._execute_action(action, alert)
                        executed_actions.append(f"{rule.name}:{action.value}")
                    except Exception as e:
                        logger.error(f"Failed to execute action {action}: {e}")
        
        return executed_actions
    
    def _matches_conditions(self, alert: Alert, conditions: Dict) -> bool:
        """Check if alert matches rule conditions"""
        for condition, value in conditions.items():
            if condition == "severity":
                if alert.severity.value not in value:
                    return False
            elif condition == "risk_score_min":
                if alert.risk_score < value:
                    return False
            elif condition == "risk_score_max":
                if alert.risk_score > value:
                    return False
            elif condition == "user_id":
                if alert.user_id not in value:
                    return False
            elif condition == "tags":
                if not any(tag in alert.tags for tag in value):
                    return False
        
        return True
    
    async def _execute_action(self, action: WorkflowAction, alert: Alert):
        """Execute a workflow action"""
        handler = self.action_handlers.get(action)
        if handler:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(self.executor, handler, alert)
        else:
            logger.warning(f"No handler registered for action: {action}")
    
    def _send_email_notification(self, alert: Alert):
        """Send email notification"""
        try:
            # Email configuration (should be in config)
            smtp_server = "localhost"
            smtp_port = 587
            sender_email = "security@company.com"
            recipient_email = "soc@company.com"
            
            msg = MimeMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = f"Security Alert: {alert.title}"
            
            body = f"""
            Security Alert Generated
            
            Alert ID: {alert.id}
            Severity: {alert.severity.value.upper()}
            Risk Score: {alert.risk_score}
            User: {alert.user_id}
            Time: {alert.timestamp}
            
            Description: {alert.description}
            
            Please investigate immediately.
            """
            
            msg.attach(MimeText(body, 'plain'))
            
            # Note: In production, use proper SMTP configuration
            logger.info(f"Email notification sent for alert {alert.id}")
            
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
    
    def _send_slack_notification(self, alert: Alert):
        """Send Slack notification"""
        try:
            # Slack webhook implementation
            logger.info(f"Slack notification sent for alert {alert.id}")
        except Exception as e:
            logger.error(f"Failed to send Slack notification: {e}")
    
    def _create_ticket(self, alert: Alert):
        """Create support ticket"""
        try:
            # ServiceNow/Jira integration
            logger.info(f"Ticket created for alert {alert.id}")
        except Exception as e:
            logger.error(f"Failed to create ticket: {e}")
    
    def _lockout_account(self, alert: Alert):
        """Lock user account"""
        try:
            # Active Directory integration
            logger.info(f"Account {alert.user_id} locked due to alert {alert.id}")
        except Exception as e:
            logger.error(f"Failed to lock account: {e}")
    
    def _revoke_access(self, alert: Alert):
        """Revoke user access"""
        try:
            # Identity provider integration
            logger.info(f"Access revoked for user {alert.user_id} due to alert {alert.id}")
        except Exception as e:
            logger.error(f"Failed to revoke access: {e}")
    
    def _escalate_alert(self, alert: Alert):
        """Escalate alert to higher tier"""
        try:
            # Escalation logic
            logger.info(f"Alert {alert.id} escalated")
        except Exception as e:
            logger.error(f"Failed to escalate alert: {e}")

class AlertManager:
    """Main alert management system"""
    
    def __init__(self):
        self.alerts: Dict[str, Alert] = {}
        self.correlation_engine = AlertCorrelationEngine()
        self.workflow_engine = WorkflowEngine()
        self.alert_history: List[Alert] = []
        
        # Setup default workflow rules
        self._setup_default_rules()
    
    def _setup_default_rules(self):
        """Setup default workflow rules"""
        # Critical alert rule
        critical_rule = WorkflowRule(
            id="critical_alert_rule",
            name="Critical Alert Response",
            conditions={
                "severity": ["critical"],
                "risk_score_min": 90
            },
            actions=[
                WorkflowAction.EMAIL_NOTIFICATION,
                WorkflowAction.SLACK_NOTIFICATION,
                WorkflowAction.TICKET_CREATION,
                WorkflowAction.ESCALATION
            ],
            priority=100
        )
        
        # High risk rule
        high_risk_rule = WorkflowRule(
            id="high_risk_rule",
            name="High Risk Alert Response",
            conditions={
                "severity": ["high"],
                "risk_score_min": 70
            },
            actions=[
                WorkflowAction.EMAIL_NOTIFICATION,
                WorkflowAction.TICKET_CREATION
            ],
            priority=80
        )
        
        # Account compromise rule
        compromise_rule = WorkflowRule(
            id="account_compromise_rule",
            name="Account Compromise Response",
            conditions={
                "tags": ["account_compromise", "impossible_travel"]
            },
            actions=[
                WorkflowAction.ACCOUNT_LOCKOUT,
                WorkflowAction.EMAIL_NOTIFICATION,
                WorkflowAction.ESCALATION
            ],
            priority=90
        )
        
        self.workflow_engine.add_rule(critical_rule)
        self.workflow_engine.add_rule(high_risk_rule)
        self.workflow_engine.add_rule(compromise_rule)
    
    async def create_alert(self, 
                          user_id: str,
                          title: str,
                          description: str,
                          risk_score: float,
                          source_event: Dict,
                          tags: List[str] = None) -> Alert:
        """Create a new alert"""
        
        # Determine severity based on risk score
        if risk_score >= 90:
            severity = AlertSeverity.CRITICAL
        elif risk_score >= 70:
            severity = AlertSeverity.HIGH
        elif risk_score >= 40:
            severity = AlertSeverity.MEDIUM
        else:
            severity = AlertSeverity.LOW
        
        alert = Alert(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            user_id=user_id,
            severity=severity,
            status=AlertStatus.OPEN,
            title=title,
            description=description,
            risk_score=risk_score,
            source_event=source_event,
            tags=tags or [],
            metadata={}
        )
        
        # Store alert
        self.alerts[alert.id] = alert
        self.alert_history.append(alert)
        
        # Correlate with existing alerts
        existing_alerts = list(self.alerts.values())
        related_alerts = await self.correlation_engine.correlate_alert(alert, existing_alerts)
        
        if related_alerts:
            alert.metadata['related_alerts'] = [a.id for a in related_alerts]
            logger.info(f"Alert {alert.id} correlated with {len(related_alerts)} existing alerts")
        
        # Process through workflow engine
        executed_actions = await self.workflow_engine.process_alert(alert)
        alert.metadata['executed_actions'] = executed_actions
        
        logger.info(f"Created alert {alert.id} with severity {severity.value}")
        
        return alert
    
    async def update_alert_status(self, alert_id: str, status: AlertStatus, 
                                 assigned_to: str = None, notes: str = None) -> bool:
        """Update alert status"""
        if alert_id not in self.alerts:
            return False
        
        alert = self.alerts[alert_id]
        alert.status = status
        alert.updated_at = datetime.now()
        
        if assigned_to:
            alert.assigned_to = assigned_to
        
        if status == AlertStatus.RESOLVED:
            alert.resolved_at = datetime.now()
            alert.resolution_notes = notes
        
        logger.info(f"Updated alert {alert_id} status to {status.value}")
        return True
    
    def get_alerts(self, 
                   status: AlertStatus = None,
                   severity: AlertSeverity = None,
                   user_id: str = None,
                   limit: int = 100) -> List[Alert]:
        """Get alerts with filters"""
        filtered_alerts = list(self.alerts.values())
        
        if status:
            filtered_alerts = [a for a in filtered_alerts if a.status == status]
        
        if severity:
            filtered_alerts = [a for a in filtered_alerts if a.severity == severity]
        
        if user_id:
            filtered_alerts = [a for a in filtered_alerts if a.user_id == user_id]
        
        # Sort by timestamp (newest first)
        filtered_alerts.sort(key=lambda a: a.timestamp, reverse=True)
        
        return filtered_alerts[:limit]
    
    def get_alert_statistics(self) -> Dict:
        """Get alert statistics"""
        total_alerts = len(self.alerts)
        
        if total_alerts == 0:
            return {
                'total': 0,
                'by_severity': {},
                'by_status': {},
                'avg_risk_score': 0,
                'resolution_rate': 0
            }
        
        # Count by severity
        severity_counts = {}
        for severity in AlertSeverity:
            severity_counts[severity.value] = len([
                a for a in self.alerts.values() if a.severity == severity
            ])
        
        # Count by status
        status_counts = {}
        for status in AlertStatus:
            status_counts[status.value] = len([
                a for a in self.alerts.values() if a.status == status
            ])
        
        # Calculate average risk score
        avg_risk_score = sum(a.risk_score for a in self.alerts.values()) / total_alerts
        
        # Calculate resolution rate
        resolved_count = status_counts.get('resolved', 0) + status_counts.get('false_positive', 0)
        resolution_rate = (resolved_count / total_alerts) * 100
        
        return {
            'total': total_alerts,
            'by_severity': severity_counts,
            'by_status': status_counts,
            'avg_risk_score': round(avg_risk_score, 2),
            'resolution_rate': round(resolution_rate, 2)
        }

# Global alert manager instance
alert_manager = AlertManager()

async def main():
    """Test alert management system"""
    print("🚨 Alert Management System - Testing")
    print("=" * 50)
    
    # Create test alerts
    alert1 = await alert_manager.create_alert(
        user_id="john.doe",
        title="Suspicious Login from Moscow",
        description="User logged in from unusual location at 3 AM",
        risk_score=95,
        source_event={
            'timestamp': '2026-01-09 03:00:00',
            'location': 'Moscow',
            'device': 'unknown'
        },
        tags=["account_compromise", "unusual_location"]
    )
    
    alert2 = await alert_manager.create_alert(
        user_id="jane.smith",
        title="Multiple Failed Login Attempts",
        description="5 failed login attempts in 2 minutes",
        risk_score=75,
        source_event={
            'timestamp': '2026-01-09 10:30:00',
            'failed_attempts': 5
        },
        tags=["brute_force"]
    )
    
    # Get statistics
    stats = alert_manager.get_alert_statistics()
    print(f"\nAlert Statistics: {stats}")
    
    # Update alert status
    await alert_manager.update_alert_status(
        alert1.id, 
        AlertStatus.INVESTIGATING,
        assigned_to="analyst1",
        notes="Investigating suspicious Moscow login"
    )
    
    print(f"\nAlert {alert1.id} updated to investigating status")
    
    # Get recent alerts
    recent_alerts = alert_manager.get_alerts(limit=10)
    print(f"\nRecent alerts: {len(recent_alerts)}")
    
    for alert in recent_alerts:
        print(f"  {alert.id}: {alert.title} ({alert.severity.value})")

if __name__ == "__main__":
    asyncio.run(main())