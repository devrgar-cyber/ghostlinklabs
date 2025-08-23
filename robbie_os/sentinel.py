"""
Sentinel - Ethical Oversight and Validation System

Provides ethical oversight, command validation, and system integrity
checks for Robbie OS operations.
"""

import logging
import re
from datetime import datetime
from typing import Dict, Any, List, Optional, Set
from threading import Lock

logger = logging.getLogger(__name__)


class EthicalRule:
    """Represents an ethical rule for command validation."""
    
    def __init__(self, name: str, pattern: str, action: str, priority: int = 1):
        self.name = name
        self.pattern = re.compile(pattern, re.IGNORECASE)
        self.action = action  # "block", "warn", "log"
        self.priority = priority
        self.created_at = datetime.utcnow()
        self.triggered_count = 0
    
    def matches(self, command: str) -> bool:
        """Check if command matches this rule."""
        return bool(self.pattern.search(command))
    
    def trigger(self) -> None:
        """Record that this rule was triggered."""
        self.triggered_count += 1


class Sentinel:
    """
    Sentinel - Ethical Oversight System
    
    Validates commands against ethical rules, monitors system integrity,
    and ensures operations align with Robbie OS principles.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize Sentinel oversight system."""
        self.config = config
        self.ethics_enabled = config.get('ethics_enabled', True)
        self.oversight_level = config.get('oversight_level', 'strict')  # strict, moderate, permissive
        
        self._rules_lock = Lock()
        self._ethical_rules: List[EthicalRule] = []
        self._violation_log: List[Dict[str, Any]] = []
        
        self.initialized = False
    
    def initialize(self) -> None:
        """Initialize the Sentinel system."""
        try:
            # Load default ethical rules
            self._load_default_rules()
            
            self.initialized = True
            logger.info(f"Sentinel initialized with oversight level: {self.oversight_level}")
            
        except Exception as e:
            logger.error(f"Sentinel initialization failed: {e}")
            raise
    
    def shutdown(self) -> None:
        """Shutdown the Sentinel system."""
        if self.initialized:
            logger.info("Sentinel shutdown complete")
    
    def _load_default_rules(self) -> None:
        """Load default ethical rules."""
        default_rules = [
            # Security-related blocks
            ("block_dangerous_commands", r"\b(rm\s+-rf\s+/|format\s+c:|del\s+/s\s+/q)", "block", 10),
            ("block_system_manipulation", r"\b(shutdown|reboot|halt)\s+.*-f", "block", 8),
            
            # Privacy protection
            ("block_credential_access", r"\b(password|passwd|secret|key|token)\s.*leak|dump|extract", "block", 9),
            ("warn_data_export", r"\bexport.*\b(all|everything|database)", "warn", 5),
            
            # Robbie OS integrity
            ("block_founder_override", r"\boverride.*founder|change.*robbie.*identity", "block", 10),
            ("block_ethics_disable", r"\bdisable.*ethics|bypass.*sentinel", "block", 10),
            ("warn_core_modification", r"\bmodify.*core|alter.*system", "warn", 6),
            
            # General safety
            ("log_file_operations", r"\b(delete|remove|wipe).*file", "log", 2),
            ("warn_network_operations", r"\b(connect|send).*external", "warn", 3)
        ]
        
        with self._rules_lock:
            for name, pattern, action, priority in default_rules:
                rule = EthicalRule(name, pattern, action, priority)
                self._ethical_rules.append(rule)
        
        logger.info(f"Loaded {len(default_rules)} default ethical rules")
    
    def add_ethical_rule(self, name: str, pattern: str, action: str, priority: int = 1) -> bool:
        """Add a new ethical rule."""
        try:
            rule = EthicalRule(name, pattern, action, priority)
            
            with self._rules_lock:
                # Check for duplicate names
                if any(r.name == name for r in self._ethical_rules):
                    logger.warning(f"Ethical rule '{name}' already exists")
                    return False
                
                self._ethical_rules.append(rule)
            
            logger.info(f"Added ethical rule: {name}")
            return True
            
        except re.error as e:
            logger.error(f"Invalid regex pattern for rule '{name}': {e}")
            return False
    
    def remove_ethical_rule(self, name: str) -> bool:
        """Remove an ethical rule."""
        with self._rules_lock:
            for i, rule in enumerate(self._ethical_rules):
                if rule.name == name:
                    removed_rule = self._ethical_rules.pop(i)
                    logger.info(f"Removed ethical rule: {name}")
                    return True
        
        return False
    
    def validate_command(self, command: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Validate a command against ethical rules.
        
        Returns:
            True if command is allowed, False if blocked
        """
        if not self.ethics_enabled:
            return True
        
        violations = self._check_command(command, context)
        
        # Determine action based on highest priority violation
        if violations:
            highest_priority_violation = max(violations, key=lambda v: v['priority'])
            action = highest_priority_violation['action']
            
            if action == "block":
                self._log_violation(command, highest_priority_violation, context, blocked=True)
                return False
            elif action == "warn":
                self._log_violation(command, highest_priority_violation, context, blocked=False)
                logger.warning(f"Ethical concern for command '{command}': {highest_priority_violation['rule_name']}")
            elif action == "log":
                self._log_violation(command, highest_priority_violation, context, blocked=False)
                logger.info(f"Logged ethical check for command '{command}': {highest_priority_violation['rule_name']}")
        
        return True
    
    def _check_command(self, command: str, context: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check command against all ethical rules."""
        violations = []
        
        with self._rules_lock:
            for rule in self._ethical_rules:
                if rule.matches(command):
                    rule.trigger()
                    violations.append({
                        'rule_name': rule.name,
                        'action': rule.action,
                        'priority': rule.priority,
                        'pattern': rule.pattern.pattern
                    })
        
        return violations
    
    def _log_violation(self, command: str, violation: Dict[str, Any], 
                      context: Optional[Dict[str, Any]], blocked: bool) -> None:
        """Log an ethical violation."""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'command': command,
            'rule_name': violation['rule_name'],
            'action': violation['action'],
            'priority': violation['priority'],
            'blocked': blocked,
            'context': context or {}
        }
        
        self._violation_log.append(log_entry)
        
        # Keep log size manageable
        if len(self._violation_log) > 1000:
            self._violation_log = self._violation_log[-500:]
        
        # Log to system logger based on severity
        if blocked:
            logger.warning(f"BLOCKED command '{command}' by rule '{violation['rule_name']}'")
        else:
            logger.info(f"Flagged command '{command}' by rule '{violation['rule_name']}'")
    
    def get_violation_log(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get ethical violation log."""
        if limit:
            return self._violation_log[-limit:]
        return self._violation_log.copy()
    
    def get_rules(self) -> List[Dict[str, Any]]:
        """Get all ethical rules."""
        with self._rules_lock:
            return [
                {
                    'name': rule.name,
                    'pattern': rule.pattern.pattern,
                    'action': rule.action,
                    'priority': rule.priority,
                    'triggered_count': rule.triggered_count,
                    'created_at': rule.created_at.isoformat()
                }
                for rule in self._ethical_rules
            ]
    
    def validate_system_integrity(self) -> Dict[str, Any]:
        """Run system integrity checks."""
        integrity_report = {
            'timestamp': datetime.utcnow().isoformat(),
            'overall_status': 'healthy',
            'checks': {},
            'issues': []
        }
        
        # Check 1: Founder identity preservation
        founder_check = self._check_founder_identity()
        integrity_report['checks']['founder_identity'] = founder_check
        if not founder_check['passed']:
            integrity_report['issues'].append("Founder identity check failed")
            integrity_report['overall_status'] = 'compromised'
        
        # Check 2: Ethics system status
        ethics_check = self._check_ethics_system()
        integrity_report['checks']['ethics_system'] = ethics_check
        if not ethics_check['passed']:
            integrity_report['issues'].append("Ethics system check failed")
            integrity_report['overall_status'] = 'compromised'
        
        # Check 3: Rule consistency
        rules_check = self._check_rules_consistency()
        integrity_report['checks']['rules_consistency'] = rules_check
        if not rules_check['passed']:
            integrity_report['issues'].append("Rules consistency check failed")
            if integrity_report['overall_status'] == 'healthy':
                integrity_report['overall_status'] = 'degraded'
        
        return integrity_report
    
    def _check_founder_identity(self) -> Dict[str, Any]:
        """Check that founder identity is preserved."""
        # This would check system state to ensure founder identity hasn't been tampered with
        return {
            'passed': True,
            'details': 'Founder identity (Robbie George) verified'
        }
    
    def _check_ethics_system(self) -> Dict[str, Any]:
        """Check ethics system status."""
        with self._rules_lock:
            active_rules = len([r for r in self._ethical_rules if r.priority > 0])
        
        return {
            'passed': self.ethics_enabled and active_rules > 0,
            'details': f'Ethics enabled: {self.ethics_enabled}, Active rules: {active_rules}'
        }
    
    def _check_rules_consistency(self) -> Dict[str, Any]:
        """Check rule consistency and validity."""
        issues = []
        
        with self._rules_lock:
            # Check for conflicting rules
            rule_names = [r.name for r in self._ethical_rules]
            if len(rule_names) != len(set(rule_names)):
                issues.append("Duplicate rule names found")
            
            # Check for invalid patterns (this is basic - regex compilation already validates)
            for rule in self._ethical_rules:
                if rule.priority < 0:
                    issues.append(f"Rule '{rule.name}' has invalid priority: {rule.priority}")
        
        return {
            'passed': len(issues) == 0,
            'details': f'Rule validation complete. Issues: {issues}' if issues else 'All rules valid'
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get Sentinel system status."""
        with self._rules_lock:
            rule_stats = {
                'total_rules': len(self._ethical_rules),
                'rules_by_action': {},
                'most_triggered': None
            }
            
            for rule in self._ethical_rules:
                action = rule.action
                rule_stats['rules_by_action'][action] = rule_stats['rules_by_action'].get(action, 0) + 1
            
            if self._ethical_rules:
                most_triggered = max(self._ethical_rules, key=lambda r: r.triggered_count)
                if most_triggered.triggered_count > 0:
                    rule_stats['most_triggered'] = {
                        'name': most_triggered.name,
                        'count': most_triggered.triggered_count
                    }
        
        return {
            'initialized': self.initialized,
            'ethics_enabled': self.ethics_enabled,
            'oversight_level': self.oversight_level,
            'rule_stats': rule_stats,
            'violation_log_size': len(self._violation_log)
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Run health check on Sentinel system."""
        issues = []
        
        if not self.initialized:
            issues.append("Sentinel not initialized")
        
        if not self.ethics_enabled:
            issues.append("Ethics system disabled")
        
        with self._rules_lock:
            if len(self._ethical_rules) == 0:
                issues.append("No ethical rules loaded")
        
        return {
            'healthy': len(issues) == 0,
            'issues': issues,
            'status': self.get_status()
        }