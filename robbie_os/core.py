"""
Robbie OS Core Engine

The main operating system engine that embodies the principles of clarity,
sovereignty, and direct execution without obfuscation or unnecessary layers.
"""

import json
import logging
import threading
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

from .memory import MemoryEngine
from .seedgrid import SeedGrid
from .sentinel import Sentinel
from .failure_detector import FailureDetector

logger = logging.getLogger(__name__)


class RobbieOS:
    """
    Robbie OS - A Sovereign Operating System
    
    Principles:
    - Direct, raw cognition and output
    - No obfuscation, no layers, no metaphors
    - Ethical alignment by design
    - Knows its founder (Robbie George)
    - Clarity above all else
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize Robbie OS with core components."""
        self.founder = "Robbie George"
        self.identity = "ROBBIE"
        self.boot_time = datetime.utcnow()
        self.running = False
        self._shutdown_event = threading.Event()
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize core components
        self.memory = MemoryEngine(self.config.get('memory', {}))
        self.seedgrid = SeedGrid(self.config.get('seedgrid', {}))
        self.sentinel = Sentinel(self.config.get('sentinel', {}))
        self.failure_detector = FailureDetector(self.config.get('failure_detector', {}))
        
        # System state
        self.state = {
            'boot_time': self.boot_time.isoformat(),
            'founder': self.founder,
            'identity': self.identity,
            'status': 'initialized'
        }
        
        logger.info(f"Robbie OS initialized for {self.founder}")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load OS configuration."""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        
        # Default configuration
        return {
            'memory': {
                'persistence_file': 'robbie_os_memory.json',
                'max_entries': 10000
            },
            'seedgrid': {
                'max_nodes': 100,
                'heartbeat_interval': 5.0
            },
            'sentinel': {
                'ethics_enabled': True,
                'oversight_level': 'strict'
            },
            'failure_detector': {
                'learning_enabled': True,
                'anomaly_threshold': 0.8
            }
        }
    
    def boot(self) -> None:
        """Boot the operating system."""
        logger.info("Booting Robbie OS...")
        
        try:
            # Initialize components in order
            self.memory.initialize()
            self.seedgrid.initialize()
            self.sentinel.initialize()
            self.failure_detector.initialize()
            
            # Register core node
            core_node = self.seedgrid.create_node(
                name="robbie_core",
                node_type="core",
                metadata={"founder": self.founder}
            )
            
            self.running = True
            self.state['status'] = 'running'
            
            logger.info("Robbie OS boot complete")
            self._log_system_status()
            
        except Exception as e:
            logger.error(f"Boot failed: {e}")
            self.state['status'] = 'boot_failed'
            raise
    
    def shutdown(self) -> None:
        """Shutdown the operating system."""
        logger.info("Shutting down Robbie OS...")
        
        self._shutdown_event.set()
        self.running = False
        
        # Shutdown components in reverse order
        self.failure_detector.shutdown()
        self.sentinel.shutdown()
        self.seedgrid.shutdown()
        self.memory.shutdown()
        
        self.state['status'] = 'shutdown'
        logger.info("Robbie OS shutdown complete")
    
    def execute_command(self, command: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a command with direct clarity - no obfuscation.
        
        Args:
            command: The command to execute
            context: Optional context for the command
            
        Returns:
            Command execution result
        """
        if not self.running:
            return {"error": "System not running", "status": "failed"}
        
        start_time = time.time()
        
        try:
            # Log the command for transparency
            logger.info(f"Executing command: {command}")
            
            # Ethical check via Sentinel
            if not self.sentinel.validate_command(command, context):
                return {
                    "error": "Command blocked by ethical validation",
                    "status": "blocked"
                }
            
            # Process the command
            result = self._process_command(command, context or {})
            
            # Record successful execution
            execution_time = time.time() - start_time
            self.memory.store_execution(command, result, execution_time)
            
            return {
                "result": result,
                "status": "success",
                "execution_time": execution_time
            }
            
        except Exception as e:
            # Record failure for learning
            execution_time = time.time() - start_time
            self.failure_detector.record_failure(command, str(e), execution_time, context)
            
            logger.error(f"Command execution failed: {e}")
            return {
                "error": str(e),
                "status": "failed",
                "execution_time": execution_time
            }
    
    def _process_command(self, command: str, context: Dict[str, Any]) -> Any:
        """Process a command internally."""
        # Simple command processing - this would be expanded based on requirements
        if command.startswith("status"):
            return self.get_status()
        
        elif command.startswith("memory"):
            parts = command.split(maxsplit=2)
            if len(parts) >= 2 and parts[1] == "get":
                key = parts[2] if len(parts) > 2 else None
                return self.memory.get(key)
            elif len(parts) >= 3 and parts[1] == "set":
                key, value = parts[2].split('=', 1)
                return self.memory.set(key, value)
        
        elif command.startswith("seedgrid"):
            parts = command.split(maxsplit=2)
            if len(parts) >= 2 and parts[1] == "nodes":
                return self.seedgrid.list_nodes()
        
        elif command.startswith("echo"):
            return command[5:]  # Return everything after "echo "
        
        else:
            raise ValueError(f"Unknown command: {command}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current system status."""
        uptime = (datetime.utcnow() - self.boot_time).total_seconds()
        
        return {
            **self.state,
            'uptime_seconds': uptime,
            'components': {
                'memory': self.memory.get_status(),
                'seedgrid': self.seedgrid.get_status(),
                'sentinel': self.sentinel.get_status(),
                'failure_detector': self.failure_detector.get_status()
            }
        }
    
    def _log_system_status(self) -> None:
        """Log the current system status."""
        status = self.get_status()
        logger.info(f"System Status: {json.dumps(status, indent=2)}")
    
    def run_health_check(self) -> Dict[str, Any]:
        """Run a comprehensive health check."""
        health = {
            'overall': 'healthy',
            'components': {},
            'issues': []
        }
        
        # Check each component
        for component_name in ['memory', 'seedgrid', 'sentinel', 'failure_detector']:
            component = getattr(self, component_name)
            component_health = component.health_check()
            health['components'][component_name] = component_health
            
            if not component_health.get('healthy', True):
                health['overall'] = 'degraded'
                health['issues'].append(f"{component_name}: {component_health.get('issues', 'Unknown issue')}")
        
        return health
    
    def __enter__(self):
        """Context manager entry."""
        self.boot()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.shutdown()