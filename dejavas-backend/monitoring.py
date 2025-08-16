"""
Dejavas Monitoring & Observability System

Production-ready monitoring with metrics, logging, health checks,
and performance tracking for enterprise deployment.
"""

import time
import logging
import asyncio
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import psutil
import os

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Performance metrics for monitoring"""
    response_time: float = 0.0
    throughput: int = 0
    error_rate: float = 0.0
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    active_connections: int = 0
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class HealthStatus:
    """System health status"""
    status: str = "healthy"
    checks: Dict[str, bool] = field(default_factory=dict)
    last_check: datetime = field(default_factory=datetime.now)
    uptime: float = 0.0
    version: str = "1.0.0"

class SystemMonitor:
    """System resource and performance monitoring"""
    
    def __init__(self):
        self.start_time = time.time()
        self.metrics_history: List[PerformanceMetrics] = []
        self.health_status = HealthStatus()
        self.alert_thresholds = {
            "cpu_usage": 80.0,
            "memory_usage": 85.0,
            "error_rate": 5.0,
            "response_time": 2.0
        }
    
    def get_system_metrics(self) -> PerformanceMetrics:
        """Get current system performance metrics"""
        try:
            # CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            
            # Process info
            process = psutil.Process(os.getpid())
            process_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # Network connections
            connections = len(process.connections())
            
            metrics = PerformanceMetrics(
                cpu_usage=cpu_usage,
                memory_usage=memory_usage,
                active_connections=connections,
                timestamp=datetime.now()
            )
            
            # Store in history (keep last 100)
            self.metrics_history.append(metrics)
            if len(self.metrics_history) > 100:
                self.metrics_history.pop(0)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
            return PerformanceMetrics()
    
    def check_system_health(self) -> HealthStatus:
        """Check overall system health"""
        try:
            metrics = self.get_system_metrics()
            checks = {}
            
            # CPU health check
            checks["cpu"] = metrics.cpu_usage < self.alert_thresholds["cpu_usage"]
            
            # Memory health check
            checks["memory"] = metrics.memory_usage < self.alert_thresholds["memory_usage"]
            
            # Process health check
            checks["process"] = True  # Process is running
            
            # Disk health check
            disk_usage = psutil.disk_usage('/').percent
            checks["disk"] = disk_usage < 90
            
            # Network health check
            checks["network"] = True  # Basic network check
            
            # Overall health
            all_healthy = all(checks.values())
            status = "healthy" if all_healthy else "degraded"
            
            # Calculate uptime
            uptime = time.time() - self.start_time
            
            self.health_status = HealthStatus(
                status=status,
                checks=checks,
                last_check=datetime.now(),
                uptime=uptime
            )
            
            return self.health_status
            
        except Exception as e:
            logger.error(f"Error checking system health: {e}")
            return HealthStatus(status="error")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary for monitoring dashboards"""
        if not self.metrics_history:
            return {}
        
        recent_metrics = self.metrics_history[-10:]  # Last 10 measurements
        
        avg_cpu = sum(m.cpu_usage for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m.memory_usage for m in recent_metrics) / len(recent_metrics)
        avg_response_time = sum(m.response_time for m in recent_metrics) / len(recent_metrics)
        
        return {
            "current_metrics": self.get_system_metrics().__dict__,
            "averages": {
                "cpu_usage": round(avg_cpu, 2),
                "memory_usage": round(avg_memory, 2),
                "response_time": round(avg_response_time, 3)
            },
            "health_status": self.health_status.__dict__,
            "uptime_hours": round((time.time() - self.start_time) / 3600, 2),
            "metrics_count": len(self.metrics_history)
        }

class APIMonitor:
    """API performance and usage monitoring"""
    
    def __init__(self):
        self.request_counts: Dict[str, int] = {}
        self.response_times: Dict[str, List[float]] = {}
        self.error_counts: Dict[str, int] = {}
        self.start_time = time.time()
    
    def record_request(self, endpoint: str, response_time: float, success: bool = True):
        """Record API request metrics"""
        # Update request counts
        self.request_counts[endpoint] = self.request_counts.get(endpoint, 0) + 1
        
        # Update response times
        if endpoint not in self.response_times:
            self.response_times[endpoint] = []
        self.response_times[endpoint].append(response_time)
        
        # Keep only last 100 response times per endpoint
        if len(self.response_times[endpoint]) > 100:
            self.response_times[endpoint].pop(0)
        
        # Update error counts
        if not success:
            self.error_counts[endpoint] = self.error_counts.get(endpoint, 0) + 1
    
    def get_api_metrics(self) -> Dict[str, Any]:
        """Get API performance metrics"""
        total_requests = sum(self.request_counts.values())
        total_errors = sum(self.error_counts.values())
        
        # Calculate error rate
        error_rate = (total_errors / total_requests * 100) if total_requests > 0 else 0
        
        # Calculate average response times
        avg_response_times = {}
        for endpoint, times in self.response_times.items():
            if times:
                avg_response_times[endpoint] = sum(times) / len(times)
        
        return {
            "total_requests": total_requests,
            "total_errors": total_errors,
            "error_rate": round(error_rate, 2),
            "request_counts": self.request_counts,
            "error_counts": self.error_counts,
            "avg_response_times": avg_response_times,
            "uptime_hours": round((time.time() - self.start_time) / 3600, 2)
        }

class BusinessMetrics:
    """Business and feature usage metrics"""
    
    def __init__(self):
        self.feature_usage: Dict[str, int] = {}
        self.simulation_runs: int = 0
        self.content_analyses: int = 0
        self.market_insights: int = 0
        self.start_time = time.time()
    
    def record_feature_usage(self, feature: str):
        """Record feature usage"""
        self.feature_usage[feature] = self.feature_usage.get(feature, 0) + 1
    
    def record_simulation_run(self):
        """Record simulation execution"""
        self.simulation_runs += 1
    
    def record_content_analysis(self):
        """Record content analysis"""
        self.content_analyses += 1
    
    def record_market_insight(self):
        """Record market insight generation"""
        self.market_insights += 1
    
    def get_business_metrics(self) -> Dict[str, Any]:
        """Get business metrics summary"""
        total_features_used = sum(self.feature_usage.values())
        
        return {
            "feature_usage": self.feature_usage,
            "total_feature_usage": total_features_used,
            "simulation_runs": self.simulation_runs,
            "content_analyses": self.content_analyses,
            "market_insights": self.market_insights,
            "uptime_hours": round((time.time() - self.start_time) / 3600, 2),
            "usage_intensity": {
                "simulations_per_hour": round(self.simulation_runs / max(1, (time.time() - self.start_time) / 3600), 2),
                "analyses_per_hour": round(self.content_analyses / max(1, (time.time() - self.start_time) / 3600), 2)
            }
        }

class MonitoringMiddleware:
    """FastAPI middleware for request monitoring"""
    
    def __init__(self, api_monitor: APIMonitor):
        self.api_monitor = api_monitor
    
    async def __call__(self, request, call_next):
        start_time = time.time()
        
        try:
            response = await call_next(request)
            success = response.status_code < 400
        except Exception:
            success = False
            raise
        finally:
            response_time = time.time() - start_time
            endpoint = f"{request.method} {request.url.path}"
            
            self.api_monitor.record_request(endpoint, response_time, success)
        
        return response

class AlertManager:
    """Alert management for monitoring thresholds"""
    
    def __init__(self, system_monitor: SystemMonitor):
        self.system_monitor = system_monitor
        self.alerts: List[Dict[str, Any]] = []
        self.alert_history: List[Dict[str, Any]] = []
    
    def check_alerts(self) -> List[Dict[str, Any]]:
        """Check for alert conditions"""
        current_alerts = []
        metrics = self.system_monitor.get_system_metrics()
        
        # CPU alert
        if metrics.cpu_usage > self.system_monitor.alert_thresholds["cpu_usage"]:
            alert = {
                "type": "high_cpu",
                "severity": "warning",
                "message": f"CPU usage is {metrics.cpu_usage:.1f}%",
                "timestamp": datetime.now(),
                "value": metrics.cpu_usage,
                "threshold": self.system_monitor.alert_thresholds["cpu_usage"]
            }
            current_alerts.append(alert)
        
        # Memory alert
        if metrics.memory_usage > self.system_monitor.alert_thresholds["memory_usage"]:
            alert = {
                "type": "high_memory",
                "severity": "warning",
                "message": f"Memory usage is {metrics.memory_usage:.1f}%",
                "timestamp": datetime.now(),
                "value": metrics.memory_usage,
                "threshold": self.system_monitor.alert_thresholds["memory_usage"]
            }
            current_alerts.append(alert)
        
        # Update alerts
        self.alerts = current_alerts
        
        # Add to history
        for alert in current_alerts:
            self.alert_history.append(alert)
        
        # Keep only last 100 alerts in history
        if len(self.alert_history) > 100:
            self.alert_history = self.alert_history[-100:]
        
        return current_alerts
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """Get alert summary"""
        return {
            "current_alerts": len(self.alerts),
            "total_alerts": len(self.alert_history),
            "alerts_by_severity": {
                "critical": len([a for a in self.alert_history if a["severity"] == "critical"]),
                "warning": len([a for a in self.alert_history if a["severity"] == "warning"]),
                "info": len([a for a in self.alert_history if a["severity"] == "info"])
            },
            "recent_alerts": self.alert_history[-10:] if self.alert_history else []
        }

# Global monitoring instances
system_monitor = SystemMonitor()
api_monitor = APIMonitor()
business_metrics = BusinessMetrics()
alert_manager = AlertManager(system_monitor)

def get_monitoring_summary() -> Dict[str, Any]:
    """Get comprehensive monitoring summary"""
    return {
        "system": system_monitor.get_performance_summary(),
        "api": api_monitor.get_api_metrics(),
        "business": business_metrics.get_business_metrics(),
        "alerts": alert_manager.get_alert_summary(),
        "timestamp": datetime.now().isoformat()
    }

async def start_monitoring():
    """Start background monitoring tasks"""
    logger.info("🚀 Starting Dejavas monitoring system...")
    
    while True:
        try:
            # Check system health
            health_status = system_monitor.check_system_health()
            
            # Check for alerts
            alerts = alert_manager.check_alerts()
            
            # Log status every 5 minutes
            if int(time.time()) % 300 == 0:
                logger.info(f"System Status: {health_status.status}")
                logger.info(f"Active Alerts: {len(alerts)}")
                
                if alerts:
                    for alert in alerts:
                        logger.warning(f"Alert: {alert['message']}")
            
            # Wait 30 seconds before next check
            await asyncio.sleep(30)
            
        except Exception as e:
            logger.error(f"Monitoring error: {e}")
            await asyncio.sleep(60)  # Wait longer on error
