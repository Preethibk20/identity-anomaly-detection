#!/usr/bin/env python3
"""
Real-time Processing Engine - Enterprise-grade stream processing
Supports Kafka, Redis, and microsecond-level detection
"""

import asyncio
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
import numpy as np
import pandas as pd
from dataclasses import dataclass
import aioredis
import aiokafka
from concurrent.futures import ThreadPoolExecutor
import threading
import queue
import websockets
import weakref

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ProcessingMetrics:
    """Metrics for real-time processing performance"""
    events_processed: int = 0
    events_per_second: float = 0.0
    avg_processing_time: float = 0.0
    alerts_generated: int = 0
    errors_count: int = 0
    last_update: datetime = None

class CircularBuffer:
    """High-performance circular buffer for streaming data"""
    
    def __init__(self, size: int):
        self.size = size
        self.buffer = [None] * size
        self.head = 0
        self.count = 0
        self.lock = threading.Lock()
    
    def append(self, item):
        """Add item to buffer"""
        with self.lock:
            self.buffer[self.head] = item
            self.head = (self.head + 1) % self.size
            if self.count < self.size:
                self.count += 1
    
    def get_recent(self, n: int = None) -> List:
        """Get n most recent items"""
        if n is None:
            n = self.count
        
        with self.lock:
            if self.count == 0:
                return []
            
            items = []
            for i in range(min(n, self.count)):
                idx = (self.head - 1 - i) % self.size
                if self.buffer[idx] is not None:
                    items.append(self.buffer[idx])
            
            return items

class EventProcessor:
    """High-performance event processor with batching"""
    
    def __init__(self, batch_size: int = 100, flush_interval: float = 1.0):
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.event_queue = asyncio.Queue(maxsize=10000)
        self.batch_buffer = []
        self.last_flush = time.time()
        self.processing_callbacks = []
        
    def add_callback(self, callback: Callable):
        """Add processing callback"""
        self.processing_callbacks.append(callback)
    
    async def enqueue_event(self, event: Dict):
        """Add event to processing queue"""
        try:
            await self.event_queue.put(event)
        except asyncio.QueueFull:
            logger.warning("Event queue full, dropping event")
    
    async def process_events(self):
        """Process events in batches"""
        while True:
            try:
                # Get event with timeout
                try:
                    event = await asyncio.wait_for(
                        self.event_queue.get(), timeout=0.1
                    )
                    self.batch_buffer.append(event)
                except asyncio.TimeoutError:
                    pass
                
                # Check if we should flush batch
                current_time = time.time()
                should_flush = (
                    len(self.batch_buffer) >= self.batch_size or
                    (self.batch_buffer and 
                     current_time - self.last_flush >= self.flush_interval)
                )
                
                if should_flush and self.batch_buffer:
                    await self._process_batch(self.batch_buffer.copy())
                    self.batch_buffer.clear()
                    self.last_flush = current_time
                
            except Exception as e:
                logger.error(f"Error processing events: {e}")
                await asyncio.sleep(0.1)
    
    async def _process_batch(self, batch: List[Dict]):
        """Process a batch of events"""
        start_time = time.time()
        
        try:
            # Call all registered callbacks
            for callback in self.processing_callbacks:
                await callback(batch)
            
            processing_time = time.time() - start_time
            logger.debug(f"Processed batch of {len(batch)} events in {processing_time:.3f}s")
            
        except Exception as e:
            logger.error(f"Error processing batch: {e}")

class RealTimeCache:
    """High-performance Redis-based cache for real-time data"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis = None
        self.local_cache = {}
        self.cache_ttl = 300  # 5 minutes
    
    async def connect(self):
        """Connect to Redis"""
        try:
            self.redis = await aioredis.from_url(self.redis_url)
            logger.info("Connected to Redis cache")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}, using local cache")
    
    async def get(self, key: str) -> Optional[Dict]:
        """Get value from cache"""
        # Try local cache first
        if key in self.local_cache:
            value, timestamp = self.local_cache[key]
            if time.time() - timestamp < self.cache_ttl:
                return value
            else:
                del self.local_cache[key]
        
        # Try Redis
        if self.redis:
            try:
                value = await self.redis.get(key)
                if value:
                    parsed_value = json.loads(value)
                    # Update local cache
                    self.local_cache[key] = (parsed_value, time.time())
                    return parsed_value
            except Exception as e:
                logger.warning(f"Redis get error: {e}")
        
        return None
    
    async def set(self, key: str, value: Dict, ttl: int = None):
        """Set value in cache"""
        if ttl is None:
            ttl = self.cache_ttl
        
        # Update local cache
        self.local_cache[key] = (value, time.time())
        
        # Update Redis
        if self.redis:
            try:
                await self.redis.setex(key, ttl, json.dumps(value, default=str))
            except Exception as e:
                logger.warning(f"Redis set error: {e}")
    
    async def increment(self, key: str, amount: int = 1) -> int:
        """Increment counter"""
        if self.redis:
            try:
                return await self.redis.incr(key, amount)
            except Exception as e:
                logger.warning(f"Redis incr error: {e}")
        
        # Fallback to local cache
        current = self.local_cache.get(key, (0, time.time()))[0]
        new_value = current + amount
        self.local_cache[key] = (new_value, time.time())
        return new_value

class WebSocketManager:
    """Manage WebSocket connections for real-time updates"""
    
    def __init__(self):
        self.connections = weakref.WeakSet()
        self.channels = {}
    
    def add_connection(self, websocket, channels: List[str] = None):
        """Add WebSocket connection"""
        self.connections.add(websocket)
        
        if channels:
            for channel in channels:
                if channel not in self.channels:
                    self.channels[channel] = weakref.WeakSet()
                self.channels[channel].add(websocket)
    
    async def broadcast(self, message: Dict, channel: str = None):
        """Broadcast message to connections"""
        message_str = json.dumps(message, default=str)
        
        if channel and channel in self.channels:
            # Broadcast to specific channel
            connections = list(self.channels[channel])
        else:
            # Broadcast to all connections
            connections = list(self.connections)
        
        if connections:
            await asyncio.gather(
                *[self._send_safe(conn, message_str) for conn in connections],
                return_exceptions=True
            )
    
    async def _send_safe(self, websocket, message: str):
        """Send message safely to WebSocket"""
        try:
            await websocket.send(message)
        except Exception as e:
            logger.debug(f"WebSocket send error: {e}")

class RealTimeProcessor:
    """Main real-time processing engine"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        
        # Core components
        self.event_processor = EventProcessor(
            batch_size=self.config.get('batch_size', 100),
            flush_interval=self.config.get('flush_interval', 1.0)
        )
        self.cache = RealTimeCache(
            self.config.get('redis_url', 'redis://localhost:6379')
        )
        self.websocket_manager = WebSocketManager()
        
        # Metrics and monitoring
        self.metrics = ProcessingMetrics()
        self.recent_events = CircularBuffer(1000)
        self.recent_alerts = CircularBuffer(100)
        
        # ML detector (will be injected)
        self.ml_detector = None
        
        # Processing state
        self.is_running = False
        self.tasks = []
        
        # Performance tracking
        self.processing_times = CircularBuffer(1000)
        self.start_time = time.time()
        
    def set_ml_detector(self, detector):
        """Set ML detector for anomaly detection"""
        self.ml_detector = detector
    
    async def start(self):
        """Start the real-time processor"""
        if self.is_running:
            return
        
        logger.info("Starting real-time processor...")
        
        # Connect to cache
        await self.cache.connect()
        
        # Register event processing callback
        self.event_processor.add_callback(self._process_event_batch)
        
        # Start background tasks
        self.tasks = [
            asyncio.create_task(self.event_processor.process_events()),
            asyncio.create_task(self._metrics_updater()),
            asyncio.create_task(self._cleanup_task())
        ]
        
        self.is_running = True
        logger.info("Real-time processor started")
    
    async def stop(self):
        """Stop the real-time processor"""
        if not self.is_running:
            return
        
        logger.info("Stopping real-time processor...")
        
        # Cancel tasks
        for task in self.tasks:
            task.cancel()
        
        await asyncio.gather(*self.tasks, return_exceptions=True)
        
        self.is_running = False
        logger.info("Real-time processor stopped")
    
    async def process_log_entry(self, log_entry: Dict) -> Dict:
        """Process a single log entry in real-time"""
        start_time = time.time()
        
        try:
            # Add to recent events
            self.recent_events.append(log_entry)
            
            # Enqueue for batch processing
            await self.event_processor.enqueue_event(log_entry)
            
            # If ML detector is available, do immediate analysis
            if self.ml_detector:
                result = await self._analyze_with_ml(log_entry)
                
                # Cache result
                cache_key = f"analysis:{log_entry.get('user_id')}:{int(time.time())}"
                await self.cache.set(cache_key, result, ttl=3600)
                
                # Check if alert should be generated
                if result.get('risk_score', 0) >= 60:
                    await self._generate_alert(result)
                
                # Update metrics
                processing_time = time.time() - start_time
                self.processing_times.append(processing_time)
                await self.cache.increment('events_processed')
                
                return result
            
            return {'status': 'queued', 'timestamp': datetime.now().isoformat()}
            
        except Exception as e:
            logger.error(f"Error processing log entry: {e}")
            await self.cache.increment('processing_errors')
            raise
    
    async def _analyze_with_ml(self, log_entry: Dict) -> Dict:
        """Analyze log entry with ML detector"""
        try:
            user_id = log_entry.get('user_id')
            
            # Get cached user profile
            profile_key = f"profile:{user_id}"
            user_profile = await self.cache.get(profile_key)
            
            if not user_profile and hasattr(self.ml_detector, 'user_profiles'):
                user_profile = self.ml_detector.user_profiles.get(user_id, {})
                if user_profile:
                    await self.cache.set(profile_key, user_profile, ttl=1800)
            
            # Analyze with ML detector
            if hasattr(self.ml_detector, 'analyze_activity_async'):
                result = await self.ml_detector.analyze_activity_async(log_entry, user_id)
            else:
                # Fallback to sync method
                loop = asyncio.get_event_loop()
                with ThreadPoolExecutor() as executor:
                    result = await loop.run_in_executor(
                        executor, self.ml_detector.analyze_activity, log_entry, user_id
                    )
            
            return result
            
        except Exception as e:
            logger.error(f"ML analysis error: {e}")
            return {
                'error': str(e),
                'risk_score': 0,
                'risk_level': 'Unknown',
                'timestamp': log_entry.get('timestamp')
            }
    
    async def _process_event_batch(self, batch: List[Dict]):
        """Process a batch of events"""
        try:
            # Update batch processing metrics
            await self.cache.increment('batches_processed')
            await self.cache.increment('events_in_batches', len(batch))
            
            # Group events by user for efficient processing
            user_events = {}
            for event in batch:
                user_id = event.get('user_id')
                if user_id:
                    if user_id not in user_events:
                        user_events[user_id] = []
                    user_events[user_id].append(event)
            
            # Process events by user
            for user_id, events in user_events.items():
                await self._process_user_events(user_id, events)
            
        except Exception as e:
            logger.error(f"Batch processing error: {e}")
    
    async def _process_user_events(self, user_id: str, events: List[Dict]):
        """Process events for a specific user"""
        try:
            # Get user context from cache
            context_key = f"context:{user_id}"
            user_context = await self.cache.get(context_key) or {}
            
            # Update user context with new events
            user_context['recent_events'] = events
            user_context['last_activity'] = events[-1]['timestamp']
            user_context['event_count'] = user_context.get('event_count', 0) + len(events)
            
            # Detect patterns in user events
            patterns = self._detect_user_patterns(events, user_context)
            
            if patterns:
                user_context['detected_patterns'] = patterns
                
                # Generate pattern-based alerts
                for pattern in patterns:
                    if pattern.get('risk_level') in ['High', 'Critical']:
                        await self._generate_pattern_alert(user_id, pattern, events)
            
            # Update cache
            await self.cache.set(context_key, user_context, ttl=3600)
            
        except Exception as e:
            logger.error(f"User event processing error: {e}")
    
    def _detect_user_patterns(self, events: List[Dict], context: Dict) -> List[Dict]:
        """Detect patterns in user events"""
        patterns = []
        
        try:
            # Pattern 1: Rapid successive logins
            login_events = [e for e in events if e.get('action') == 'login']
            if len(login_events) >= 5:
                time_span = self._calculate_time_span(login_events)
                if time_span < 300:  # 5 minutes
                    patterns.append({
                        'type': 'rapid_logins',
                        'description': f'{len(login_events)} logins in {time_span:.0f} seconds',
                        'risk_level': 'High',
                        'events': login_events
                    })
            
            # Pattern 2: Failed login attempts
            failed_events = [e for e in events if not e.get('success', True)]
            if len(failed_events) >= 3:
                patterns.append({
                    'type': 'multiple_failures',
                    'description': f'{len(failed_events)} failed attempts',
                    'risk_level': 'Medium' if len(failed_events) < 5 else 'High',
                    'events': failed_events
                })
            
            # Pattern 3: Location hopping
            locations = list(set(e.get('location') for e in events if e.get('location')))
            if len(locations) >= 3:
                patterns.append({
                    'type': 'location_hopping',
                    'description': f'Activity from {len(locations)} different locations',
                    'risk_level': 'Medium',
                    'locations': locations
                })
            
            # Pattern 4: Off-hours activity burst
            off_hours_events = []
            for event in events:
                timestamp = pd.to_datetime(event['timestamp'])
                if timestamp.hour < 6 or timestamp.hour > 22:
                    off_hours_events.append(event)
            
            if len(off_hours_events) >= 3:
                patterns.append({
                    'type': 'off_hours_burst',
                    'description': f'{len(off_hours_events)} off-hours activities',
                    'risk_level': 'Medium',
                    'events': off_hours_events
                })
            
        except Exception as e:
            logger.error(f"Pattern detection error: {e}")
        
        return patterns
    
    def _calculate_time_span(self, events: List[Dict]) -> float:
        """Calculate time span between first and last event"""
        if len(events) < 2:
            return 0
        
        timestamps = [pd.to_datetime(e['timestamp']) for e in events]
        timestamps.sort()
        
        return (timestamps[-1] - timestamps[0]).total_seconds()
    
    async def _generate_alert(self, analysis_result: Dict):
        """Generate alert from analysis result"""
        try:
            alert = {
                'id': f"alert_{int(time.time() * 1000)}",
                'timestamp': datetime.now().isoformat(),
                'type': 'anomaly_detection',
                'user_id': analysis_result.get('user_id'),
                'risk_score': analysis_result.get('risk_score'),
                'risk_level': analysis_result.get('risk_level'),
                'description': analysis_result.get('explanation', 'Anomalous activity detected'),
                'activity': analysis_result.get('activity'),
                'features': analysis_result.get('features_used', {}),
                'source': 'ml_detector'
            }
            
            # Store alert
            self.recent_alerts.append(alert)
            alert_key = f"alert:{alert['id']}"
            await self.cache.set(alert_key, alert, ttl=86400)  # 24 hours
            
            # Update metrics
            await self.cache.increment('alerts_generated')
            
            # Broadcast to WebSocket clients
            await self.websocket_manager.broadcast(alert, channel='alerts')
            
            logger.info(f"Alert generated: {alert['id']} - {alert['risk_level']} risk")
            
        except Exception as e:
            logger.error(f"Alert generation error: {e}")
    
    async def _generate_pattern_alert(self, user_id: str, pattern: Dict, events: List[Dict]):
        """Generate alert from detected pattern"""
        try:
            alert = {
                'id': f"pattern_{int(time.time() * 1000)}",
                'timestamp': datetime.now().isoformat(),
                'type': 'pattern_detection',
                'user_id': user_id,
                'pattern_type': pattern['type'],
                'risk_level': pattern['risk_level'],
                'description': pattern['description'],
                'events_count': len(events),
                'pattern_details': pattern,
                'source': 'pattern_detector'
            }
            
            # Calculate risk score based on pattern
            risk_score = self._calculate_pattern_risk_score(pattern)
            alert['risk_score'] = risk_score
            
            # Store alert
            self.recent_alerts.append(alert)
            alert_key = f"alert:{alert['id']}"
            await self.cache.set(alert_key, alert, ttl=86400)
            
            # Update metrics
            await self.cache.increment('pattern_alerts_generated')
            
            # Broadcast to WebSocket clients
            await self.websocket_manager.broadcast(alert, channel='alerts')
            
            logger.info(f"Pattern alert generated: {alert['id']} - {pattern['type']}")
            
        except Exception as e:
            logger.error(f"Pattern alert generation error: {e}")
    
    def _calculate_pattern_risk_score(self, pattern: Dict) -> float:
        """Calculate risk score for detected pattern"""
        base_scores = {
            'rapid_logins': 70,
            'multiple_failures': 60,
            'location_hopping': 50,
            'off_hours_burst': 45
        }
        
        base_score = base_scores.get(pattern['type'], 40)
        
        # Adjust based on risk level
        if pattern['risk_level'] == 'Critical':
            return min(100, base_score * 1.4)
        elif pattern['risk_level'] == 'High':
            return min(100, base_score * 1.2)
        else:
            return base_score
    
    async def _metrics_updater(self):
        """Update performance metrics periodically"""
        while self.is_running:
            try:
                # Calculate events per second
                current_time = time.time()
                uptime = current_time - self.start_time
                
                events_processed = await self.cache.get('events_processed') or 0
                if isinstance(events_processed, dict):
                    events_processed = events_processed.get('value', 0)
                
                self.metrics.events_processed = events_processed
                self.metrics.events_per_second = events_processed / uptime if uptime > 0 else 0
                
                # Calculate average processing time
                recent_times = self.processing_times.get_recent(100)
                if recent_times:
                    self.metrics.avg_processing_time = np.mean(recent_times)
                
                # Update other metrics
                alerts_generated = await self.cache.get('alerts_generated') or 0
                if isinstance(alerts_generated, dict):
                    alerts_generated = alerts_generated.get('value', 0)
                
                self.metrics.alerts_generated = alerts_generated
                self.metrics.last_update = datetime.now()
                
                # Broadcast metrics to WebSocket clients
                await self.websocket_manager.broadcast({
                    'type': 'metrics_update',
                    'metrics': {
                        'events_processed': self.metrics.events_processed,
                        'events_per_second': round(self.metrics.events_per_second, 2),
                        'avg_processing_time': round(self.metrics.avg_processing_time * 1000, 2),  # ms
                        'alerts_generated': self.metrics.alerts_generated,
                        'uptime': round(uptime, 0)
                    }
                }, channel='metrics')
                
                await asyncio.sleep(5)  # Update every 5 seconds
                
            except Exception as e:
                logger.error(f"Metrics update error: {e}")
                await asyncio.sleep(5)
    
    async def _cleanup_task(self):
        """Cleanup old data periodically"""
        while self.is_running:
            try:
                # Clean up old cache entries
                current_time = time.time()
                
                # This is a simplified cleanup - in production, you'd use Redis SCAN
                # to iterate through keys and clean up expired entries
                
                await asyncio.sleep(300)  # Run every 5 minutes
                
            except Exception as e:
                logger.error(f"Cleanup task error: {e}")
                await asyncio.sleep(300)
    
    async def get_metrics(self) -> Dict:
        """Get current processing metrics"""
        return {
            'events_processed': self.metrics.events_processed,
            'events_per_second': round(self.metrics.events_per_second, 2),
            'avg_processing_time_ms': round(self.metrics.avg_processing_time * 1000, 2),
            'alerts_generated': self.metrics.alerts_generated,
            'uptime_seconds': round(time.time() - self.start_time, 0),
            'recent_events_count': self.recent_events.count,
            'recent_alerts_count': self.recent_alerts.count,
            'last_update': self.metrics.last_update.isoformat() if self.metrics.last_update else None
        }
    
    async def get_recent_alerts(self, limit: int = 20) -> List[Dict]:
        """Get recent alerts"""
        return self.recent_alerts.get_recent(limit)
    
    async def get_recent_events(self, limit: int = 50) -> List[Dict]:
        """Get recent events"""
        return self.recent_events.get_recent(limit)

# WebSocket handler for real-time updates
async def websocket_handler(websocket, path, processor: RealTimeProcessor):
    """Handle WebSocket connections for real-time updates"""
    try:
        # Add connection to manager
        processor.websocket_manager.add_connection(websocket, ['alerts', 'metrics'])
        
        # Send initial data
        await websocket.send(json.dumps({
            'type': 'connection_established',
            'timestamp': datetime.now().isoformat()
        }))
        
        # Keep connection alive and handle messages
        async for message in websocket:
            try:
                data = json.loads(message)
                
                if data.get('type') == 'get_metrics':
                    metrics = await processor.get_metrics()
                    await websocket.send(json.dumps({
                        'type': 'metrics_response',
                        'data': metrics
                    }))
                
                elif data.get('type') == 'get_recent_alerts':
                    alerts = await processor.get_recent_alerts(data.get('limit', 20))
                    await websocket.send(json.dumps({
                        'type': 'alerts_response',
                        'data': alerts
                    }))
                
            except json.JSONDecodeError:
                await websocket.send(json.dumps({
                    'type': 'error',
                    'message': 'Invalid JSON'
                }))
    
    except websockets.exceptions.ConnectionClosed:
        pass
    except Exception as e:
        logger.error(f"WebSocket error: {e}")

async def main():
    """Test the real-time processor"""
    print("⚡ Real-time Processor - Testing")
    print("=" * 50)
    
    # Initialize processor
    config = {
        'batch_size': 50,
        'flush_interval': 2.0,
        'redis_url': 'redis://localhost:6379'
    }
    
    processor = RealTimeProcessor(config)
    
    try:
        # Start processor
        await processor.start()
        
        # Simulate some log entries
        sample_logs = [
            {
                'timestamp': datetime.now().isoformat(),
                'user_id': 'john.doe',
                'action': 'login',
                'location': 'New York',
                'device': 'laptop',
                'success': True
            },
            {
                'timestamp': datetime.now().isoformat(),
                'user_id': 'john.doe',
                'action': 'login',
                'location': 'Moscow',
                'device': 'unknown',
                'success': True
            }
        ]
        
        # Process sample logs
        for log in sample_logs:
            result = await processor.process_log_entry(log)
            print(f"Processed: {result}")
        
        # Wait a bit for processing
        await asyncio.sleep(3)
        
        # Get metrics
        metrics = await processor.get_metrics()
        print(f"\nMetrics: {metrics}")
        
        # Get recent alerts
        alerts = await processor.get_recent_alerts()
        print(f"\nRecent alerts: {len(alerts)}")
        
    finally:
        await processor.stop()

if __name__ == "__main__":
    asyncio.run(main())