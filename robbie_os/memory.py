"""
Memory Engine for Robbie OS

Manages persistent state, execution history, and learning data.
Implements clarity principles - direct access, no obfuscation.
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from threading import Lock

logger = logging.getLogger(__name__)


class MemoryEngine:
    """
    Memory Engine - Persistent state and learning for Robbie OS
    
    Features:
    - Persistent storage of system state
    - Execution history tracking
    - Learning from patterns
    - Direct access with no obfuscation
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize memory engine."""
        self.config = config
        self.persistence_file = Path(config.get('persistence_file', 'robbie_os_memory.json'))
        self.max_entries = config.get('max_entries', 10000)
        
        self._memory_lock = Lock()
        self._memory = {
            'system_state': {},
            'execution_history': [],
            'learned_patterns': {},
            'metadata': {
                'created': datetime.utcnow().isoformat(),
                'version': '1.0.0'
            }
        }
        
        self.initialized = False
    
    def initialize(self) -> None:
        """Initialize the memory engine."""
        try:
            if self.persistence_file.exists():
                self._load_from_disk()
            else:
                logger.info("No existing memory file, starting fresh")
            
            self.initialized = True
            logger.info("Memory engine initialized")
            
        except Exception as e:
            logger.error(f"Memory initialization failed: {e}")
            raise
    
    def shutdown(self) -> None:
        """Shutdown memory engine and persist data."""
        if self.initialized:
            self._save_to_disk()
            logger.info("Memory engine shutdown complete")
    
    def _load_from_disk(self) -> None:
        """Load memory from persistent storage."""
        try:
            with open(self.persistence_file, 'r') as f:
                loaded_data = json.load(f)
            
            # Merge loaded data with defaults
            self._memory.update(loaded_data)
            logger.info(f"Loaded memory from {self.persistence_file}")
            
        except Exception as e:
            logger.error(f"Failed to load memory from disk: {e}")
            # Continue with empty memory rather than fail
    
    def _save_to_disk(self) -> None:
        """Save memory to persistent storage."""
        try:
            with self._memory_lock:
                # Create backup if file exists
                if self.persistence_file.exists():
                    backup_path = Path(str(self.persistence_file) + '.backup')
                    self.persistence_file.rename(backup_path)
                
                # Save current memory
                with open(self.persistence_file, 'w') as f:
                    json.dump(self._memory, f, indent=2, default=str)
                
                logger.debug(f"Memory saved to {self.persistence_file}")
                
        except Exception as e:
            logger.error(f"Failed to save memory to disk: {e}")
    
    def set(self, key: str, value: Any) -> None:
        """Set a value in system state memory."""
        with self._memory_lock:
            self._memory['system_state'][key] = {
                'value': value,
                'timestamp': datetime.utcnow().isoformat(),
                'type': type(value).__name__
            }
        
        logger.debug(f"Memory set: {key}")
    
    def get(self, key: Optional[str] = None) -> Any:
        """Get a value from system state memory."""
        with self._memory_lock:
            if key is None:
                return self._memory['system_state']
            
            entry = self._memory['system_state'].get(key)
            return entry['value'] if entry else None
    
    def store_execution(self, command: str, result: Any, execution_time: float) -> None:
        """Store execution history for learning and analysis."""
        with self._memory_lock:
            execution_record = {
                'timestamp': datetime.utcnow().isoformat(),
                'command': command,
                'result_type': type(result).__name__,
                'execution_time': execution_time,
                'success': True
            }
            
            self._memory['execution_history'].append(execution_record)
            
            # Limit history size
            if len(self._memory['execution_history']) > self.max_entries:
                self._memory['execution_history'] = self._memory['execution_history'][-self.max_entries:]
        
        logger.debug(f"Stored execution: {command}")
    
    def store_failure(self, command: str, error: str, execution_time: float, context: Optional[Dict[str, Any]] = None) -> None:
        """Store failure information for learning."""
        with self._memory_lock:
            failure_record = {
                'timestamp': datetime.utcnow().isoformat(),
                'command': command,
                'error': error,
                'execution_time': execution_time,
                'context': context,
                'success': False
            }
            
            self._memory['execution_history'].append(failure_record)
            
            # Learn from failure patterns
            self._learn_from_failure(command, error, context)
        
        logger.debug(f"Stored failure: {command}")
    
    def _learn_from_failure(self, command: str, error: str, context: Optional[Dict[str, Any]]) -> None:
        """Learn patterns from failures."""
        pattern_key = f"failure_pattern_{hash(command + error) % 1000000}"
        
        if pattern_key not in self._memory['learned_patterns']:
            self._memory['learned_patterns'][pattern_key] = {
                'command_pattern': command[:50],  # First 50 chars
                'error_type': error.split(':')[0] if ':' in error else error,
                'occurrences': 0,
                'first_seen': datetime.utcnow().isoformat()
            }
        
        self._memory['learned_patterns'][pattern_key]['occurrences'] += 1
        self._memory['learned_patterns'][pattern_key]['last_seen'] = datetime.utcnow().isoformat()
    
    def get_execution_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get execution history."""
        with self._memory_lock:
            history = self._memory['execution_history']
            return history[-limit:] if limit else history
    
    def get_learned_patterns(self) -> Dict[str, Any]:
        """Get learned patterns."""
        with self._memory_lock:
            return self._memory['learned_patterns'].copy()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        with self._memory_lock:
            total_executions = len(self._memory['execution_history'])
            successful_executions = sum(1 for ex in self._memory['execution_history'] if ex.get('success', False))
            failed_executions = total_executions - successful_executions
            
            return {
                'total_executions': total_executions,
                'successful_executions': successful_executions,
                'failed_executions': failed_executions,
                'success_rate': successful_executions / total_executions if total_executions > 0 else 0,
                'learned_patterns': len(self._memory['learned_patterns']),
                'state_entries': len(self._memory['system_state'])
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get memory engine status."""
        return {
            'initialized': self.initialized,
            'persistence_file': str(self.persistence_file),
            'stats': self.get_stats()
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Run health check on memory engine."""
        issues = []
        
        if not self.initialized:
            issues.append("Memory engine not initialized")
        
        if not self.persistence_file.parent.exists():
            issues.append("Persistence directory does not exist")
        
        return {
            'healthy': len(issues) == 0,
            'issues': issues,
            'status': self.get_status()
        }
    
    def clear_history(self) -> None:
        """Clear execution history (for maintenance)."""
        with self._memory_lock:
            self._memory['execution_history'].clear()
        logger.info("Execution history cleared")
    
    def backup_memory(self, backup_path: Optional[str] = None) -> str:
        """Create a backup of current memory."""
        if not backup_path:
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            backup_path = f"robbie_os_memory_backup_{timestamp}.json"
        
        backup_file = Path(backup_path)
        
        with self._memory_lock:
            with open(backup_file, 'w') as f:
                json.dump(self._memory, f, indent=2, default=str)
        
        logger.info(f"Memory backup created: {backup_file}")
        return str(backup_file)