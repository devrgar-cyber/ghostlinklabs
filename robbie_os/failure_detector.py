"""
Failure Detector - Anomaly Detection and Learning System

Detects patterns in failures, learns from anomalies, and provides
insights for system improvement.
"""

import logging
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from collections import defaultdict, deque
from threading import Lock
import hashlib
import statistics

logger = logging.getLogger(__name__)


class AnomalyPattern:
    """Represents a detected anomaly pattern."""
    
    def __init__(self, pattern_id: str, command_signature: str, error_type: str):
        self.pattern_id = pattern_id
        self.command_signature = command_signature
        self.error_type = error_type
        self.occurrences = 1
        self.first_seen = datetime.utcnow()
        self.last_seen = datetime.utcnow()
        self.contexts: List[Dict[str, Any]] = []
        self.severity_score = 1.0
    
    def update(self, context: Optional[Dict[str, Any]] = None):
        """Update pattern with new occurrence."""
        self.occurrences += 1
        self.last_seen = datetime.utcnow()
        if context:
            self.contexts.append(context)
            # Keep only recent contexts
            if len(self.contexts) > 10:
                self.contexts = self.contexts[-10:]
        
        # Update severity based on frequency
        self._calculate_severity()
    
    def _calculate_severity(self):
        """Calculate severity score based on occurrence patterns."""
        # Base severity on frequency
        frequency_score = min(self.occurrences / 10.0, 5.0)
        
        # Recency boost - more recent = more severe
        hours_since_last = (datetime.utcnow() - self.last_seen).total_seconds() / 3600
        recency_score = max(0, 2.0 - (hours_since_last / 24))  # Decay over days
        
        self.severity_score = frequency_score + recency_score


class FailureDetector:
    """
    Failure Detector - Learn from failures and detect anomalies
    
    Analyzes failure patterns, detects anomalies, and provides
    insights for system improvement and prevention.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize failure detector."""
        self.config = config
        self.learning_enabled = config.get('learning_enabled', True)
        self.anomaly_threshold = config.get('anomaly_threshold', 0.8)
        self.max_pattern_history = config.get('max_pattern_history', 1000)
        
        self._patterns_lock = Lock()
        self._anomaly_patterns: Dict[str, AnomalyPattern] = {}
        self._failure_history: deque = deque(maxlen=self.max_pattern_history)
        
        # Statistics tracking
        self._failure_stats = {
            'total_failures': 0,
            'failures_by_type': defaultdict(int),
            'failures_by_hour': defaultdict(int),
            'avg_failure_rate': 0.0
        }
        
        self.initialized = False
    
    def initialize(self) -> None:
        """Initialize the failure detector."""
        try:
            self.initialized = True
            logger.info("Failure detector initialized")
            
        except Exception as e:
            logger.error(f"Failure detector initialization failed: {e}")
            raise
    
    def shutdown(self) -> None:
        """Shutdown the failure detector."""
        if self.initialized:
            logger.info("Failure detector shutdown complete")
    
    def record_failure(self, command: str, error: str, execution_time: float, 
                      context: Optional[Dict[str, Any]] = None) -> str:
        """
        Record a failure for analysis and learning.
        
        Returns:
            Pattern ID if anomaly detected, None otherwise
        """
        if not self.learning_enabled:
            return None
        
        failure_record = {
            'timestamp': datetime.utcnow(),
            'command': command,
            'error': error,
            'execution_time': execution_time,
            'context': context or {}
        }
        
        # Add to history
        self._failure_history.append(failure_record)
        
        # Update statistics
        self._update_failure_stats(error)
        
        # Detect and learn patterns
        pattern_id = self._analyze_failure_pattern(command, error, context)
        
        logger.debug(f"Recorded failure for command: {command[:50]}...")
        return pattern_id
    
    def _update_failure_stats(self, error: str) -> None:
        """Update failure statistics."""
        self._failure_stats['total_failures'] += 1
        
        # Categorize error type
        error_type = self._categorize_error(error)
        self._failure_stats['failures_by_type'][error_type] += 1
        
        # Track by hour
        current_hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        self._failure_stats['failures_by_hour'][current_hour] += 1
        
        # Update average failure rate (failures per hour over last 24 hours)
        self._calculate_failure_rate()
    
    def _categorize_error(self, error: str) -> str:
        """Categorize error into types."""
        error_lower = error.lower()
        
        if 'permission' in error_lower or 'access' in error_lower:
            return 'permission'
        elif 'timeout' in error_lower:
            return 'timeout'
        elif 'connection' in error_lower or 'network' in error_lower:
            return 'network'
        elif 'syntax' in error_lower or 'invalid' in error_lower:
            return 'syntax'
        elif 'not found' in error_lower or 'missing' in error_lower:
            return 'not_found'
        elif 'memory' in error_lower or 'overflow' in error_lower:
            return 'resource'
        else:
            return 'other'
    
    def _calculate_failure_rate(self) -> None:
        """Calculate average failure rate over recent history."""
        now = datetime.utcnow()
        cutoff = now - timedelta(hours=24)
        
        recent_failures = sum(
            1 for record in self._failure_history 
            if record['timestamp'] > cutoff
        )
        
        self._failure_stats['avg_failure_rate'] = recent_failures / 24.0  # failures per hour
    
    def _analyze_failure_pattern(self, command: str, error: str, 
                                context: Optional[Dict[str, Any]]) -> Optional[str]:
        """Analyze failure for patterns and anomalies."""
        # Create command signature (generalized version)
        command_signature = self._create_command_signature(command)
        error_type = self._categorize_error(error)
        
        # Create pattern ID
        pattern_content = f"{command_signature}:{error_type}"
        pattern_id = hashlib.md5(pattern_content.encode()).hexdigest()[:12]
        
        with self._patterns_lock:
            if pattern_id in self._anomaly_patterns:
                # Update existing pattern
                pattern = self._anomaly_patterns[pattern_id]
                pattern.update(context)
            else:
                # Create new pattern
                pattern = AnomalyPattern(pattern_id, command_signature, error_type)
                if context:
                    pattern.contexts.append(context)
                self._anomaly_patterns[pattern_id] = pattern
            
            # Check if this is an anomaly (based on threshold)
            if pattern.severity_score >= self.anomaly_threshold:
                logger.warning(f"Anomaly detected: {pattern_content} (severity: {pattern.severity_score:.2f})")
                return pattern_id
        
        return None
    
    def _create_command_signature(self, command: str) -> str:
        """Create a generalized signature of the command."""
        # Replace specific values with placeholders
        import re
        
        # Replace numbers with <NUM>
        signature = re.sub(r'\b\d+\b', '<NUM>', command)
        
        # Replace quoted strings with <STR>
        signature = re.sub(r'"[^"]*"', '<STR>', signature)
        signature = re.sub(r"'[^']*'", '<STR>', signature)
        
        # Replace file paths with <PATH>
        signature = re.sub(r'\b(/[^\s]*|[A-Za-z]:\\[^\s]*)', '<PATH>', signature)
        
        # Replace URLs with <URL>
        signature = re.sub(r'https?://[^\s]+', '<URL>', signature)
        
        return signature[:100]  # Limit length
    
    def get_anomaly_patterns(self, min_severity: float = 0.0, 
                           limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get detected anomaly patterns."""
        with self._patterns_lock:
            patterns = []
            for pattern in self._anomaly_patterns.values():
                if pattern.severity_score >= min_severity:
                    patterns.append({
                        'pattern_id': pattern.pattern_id,
                        'command_signature': pattern.command_signature,
                        'error_type': pattern.error_type,
                        'occurrences': pattern.occurrences,
                        'severity_score': pattern.severity_score,
                        'first_seen': pattern.first_seen.isoformat(),
                        'last_seen': pattern.last_seen.isoformat(),
                        'recent_contexts': pattern.contexts[-3:] if pattern.contexts else []
                    })
            
            # Sort by severity, then by recency
            patterns.sort(key=lambda p: (p['severity_score'], p['last_seen']), reverse=True)
            
            if limit:
                patterns = patterns[:limit]
        
        return patterns
    
    def get_failure_insights(self) -> Dict[str, Any]:
        """Get insights about failure patterns."""
        insights = {
            'summary': {
                'total_failures': self._failure_stats['total_failures'],
                'avg_failure_rate': self._failure_stats['avg_failure_rate'],
                'total_patterns': len(self._anomaly_patterns)
            },
            'top_error_types': [],
            'trending_patterns': [],
            'recommendations': []
        }
        
        # Top error types
        sorted_error_types = sorted(
            self._failure_stats['failures_by_type'].items(),
            key=lambda x: x[1], reverse=True
        )
        insights['top_error_types'] = [
            {'type': error_type, 'count': count}
            for error_type, count in sorted_error_types[:5]
        ]
        
        # Trending patterns (high severity, recent)
        insights['trending_patterns'] = self.get_anomaly_patterns(min_severity=1.0, limit=5)
        
        # Generate recommendations
        insights['recommendations'] = self._generate_recommendations()
        
        return insights
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on failure patterns."""
        recommendations = []
        
        # Check failure rate
        if self._failure_stats['avg_failure_rate'] > 5.0:
            recommendations.append("High failure rate detected. Review system logs and consider increasing timeout values.")
        
        # Check error type patterns
        error_types = self._failure_stats['failures_by_type']
        
        if error_types.get('permission', 0) > 5:
            recommendations.append("Multiple permission errors detected. Review access controls and user permissions.")
        
        if error_types.get('timeout', 0) > 3:
            recommendations.append("Timeout errors detected. Consider increasing timeout limits or optimizing slow operations.")
        
        if error_types.get('network', 0) > 3:
            recommendations.append("Network errors detected. Check network connectivity and external service availability.")
        
        # Check for recurring patterns
        with self._patterns_lock:
            high_frequency_patterns = [
                p for p in self._anomaly_patterns.values()
                if p.occurrences >= 5
            ]
        
        if high_frequency_patterns:
            recommendations.append(f"Found {len(high_frequency_patterns)} recurring failure patterns. Consider implementing specific error handling for these cases.")
        
        if not recommendations:
            recommendations.append("System failure patterns appear normal. Continue monitoring.")
        
        return recommendations
    
    def clear_old_patterns(self, older_than_days: int = 30) -> int:
        """Clear old anomaly patterns."""
        cutoff_date = datetime.utcnow() - timedelta(days=older_than_days)
        cleared_count = 0
        
        with self._patterns_lock:
            patterns_to_remove = [
                pattern_id for pattern_id, pattern in self._anomaly_patterns.items()
                if pattern.last_seen < cutoff_date
            ]
            
            for pattern_id in patterns_to_remove:
                del self._anomaly_patterns[pattern_id]
                cleared_count += 1
        
        logger.info(f"Cleared {cleared_count} old anomaly patterns")
        return cleared_count
    
    def get_status(self) -> Dict[str, Any]:
        """Get failure detector status."""
        return {
            'initialized': self.initialized,
            'learning_enabled': self.learning_enabled,
            'anomaly_threshold': self.anomaly_threshold,
            'failure_history_size': len(self._failure_history),
            'anomaly_patterns_count': len(self._anomaly_patterns),
            'failure_stats': dict(self._failure_stats)
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Run health check on failure detector."""
        issues = []
        
        if not self.initialized:
            issues.append("Failure detector not initialized")
        
        if not self.learning_enabled:
            issues.append("Learning is disabled")
        
        # Check if we have too many high-severity patterns
        with self._patterns_lock:
            critical_patterns = sum(
                1 for pattern in self._anomaly_patterns.values()
                if pattern.severity_score >= 3.0
            )
        
        if critical_patterns > 10:
            issues.append(f"High number of critical anomaly patterns: {critical_patterns}")
        
        return {
            'healthy': len(issues) == 0,
            'issues': issues,
            'status': self.get_status()
        }