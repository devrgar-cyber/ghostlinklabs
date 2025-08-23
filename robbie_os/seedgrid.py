"""
SeedGrid - Node Management and Communication System

Manages nodes in the Robbie OS ecosystem, handles communication,
and maintains network topology with clarity and sovereignty principles.
"""

import logging
import time
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Set
from threading import Lock, Thread, Event
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class NodeType(Enum):
    """Types of nodes in the SeedGrid."""
    CORE = "core"
    WORKER = "worker"
    SENSOR = "sensor"
    MIRROR = "mirror"
    BRIDGE = "bridge"


class NodeStatus(Enum):
    """Status of nodes in the SeedGrid."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    FAILED = "failed"
    SUSPENDED = "suspended"


@dataclass
class SeedNode:
    """
    A node in the SeedGrid system.
    
    Represents a single computational unit with clear identity,
    purpose, and communication capabilities.
    """
    id: str
    name: str
    node_type: NodeType
    status: NodeStatus
    created_at: datetime
    last_heartbeat: datetime
    metadata: Dict[str, Any]
    capabilities: Set[str]
    
    def __post_init__(self):
        """Ensure proper types after initialization."""
        if isinstance(self.node_type, str):
            self.node_type = NodeType(self.node_type)
        if isinstance(self.status, str):
            self.status = NodeStatus(self.status)
        if isinstance(self.capabilities, list):
            self.capabilities = set(self.capabilities)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary representation."""
        data = asdict(self)
        data['node_type'] = self.node_type.value
        data['status'] = self.status.value
        data['created_at'] = self.created_at.isoformat()
        data['last_heartbeat'] = self.last_heartbeat.isoformat()
        data['capabilities'] = list(self.capabilities)
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SeedNode':
        """Create node from dictionary representation."""
        data = data.copy()
        data['node_type'] = NodeType(data['node_type'])
        data['status'] = NodeStatus(data['status'])
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['last_heartbeat'] = datetime.fromisoformat(data['last_heartbeat'])
        data['capabilities'] = set(data['capabilities'])
        return cls(**data)


class SeedGrid:
    """
    SeedGrid - Node Management System for Robbie OS
    
    Manages a network of nodes with clear communication protocols,
    heartbeat monitoring, and sovereign operation principles.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize SeedGrid."""
        self.config = config
        self.max_nodes = config.get('max_nodes', 100)
        self.heartbeat_interval = config.get('heartbeat_interval', 5.0)
        
        self._nodes_lock = Lock()
        self._nodes: Dict[str, SeedNode] = {}
        self._communication_log: List[Dict[str, Any]] = []
        
        # Heartbeat monitoring
        self._heartbeat_thread: Optional[Thread] = None
        self._heartbeat_stop_event = Event()
        
        self.initialized = False
    
    def initialize(self) -> None:
        """Initialize the SeedGrid system."""
        try:
            # Start heartbeat monitoring
            self._start_heartbeat_monitoring()
            
            self.initialized = True
            logger.info("SeedGrid initialized")
            
        except Exception as e:
            logger.error(f"SeedGrid initialization failed: {e}")
            raise
    
    def shutdown(self) -> None:
        """Shutdown the SeedGrid system."""
        if self.initialized:
            # Stop heartbeat monitoring
            self._heartbeat_stop_event.set()
            if self._heartbeat_thread:
                self._heartbeat_thread.join(timeout=5.0)
            
            # Mark all nodes as inactive
            with self._nodes_lock:
                for node in self._nodes.values():
                    node.status = NodeStatus.INACTIVE
            
            logger.info("SeedGrid shutdown complete")
    
    def create_node(self, name: str, node_type: str, metadata: Optional[Dict[str, Any]] = None, 
                   capabilities: Optional[List[str]] = None) -> SeedNode:
        """Create a new node in the SeedGrid."""
        node_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        node = SeedNode(
            id=node_id,
            name=name,
            node_type=NodeType(node_type),
            status=NodeStatus.ACTIVE,
            created_at=now,
            last_heartbeat=now,
            metadata=metadata or {},
            capabilities=set(capabilities or [])
        )
        
        with self._nodes_lock:
            if len(self._nodes) >= self.max_nodes:
                raise ValueError(f"Maximum nodes ({self.max_nodes}) reached")
            
            self._nodes[node_id] = node
        
        self._log_communication("NODE_CREATED", {
            "node_id": node_id,
            "name": name,
            "type": node_type
        })
        
        logger.info(f"Created node: {name} ({node_id})")
        return node
    
    def get_node(self, node_id: str) -> Optional[SeedNode]:
        """Get a node by ID."""
        with self._nodes_lock:
            return self._nodes.get(node_id)
    
    def list_nodes(self, status_filter: Optional[str] = None, 
                  type_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """List nodes with optional filtering."""
        with self._nodes_lock:
            nodes = []
            for node in self._nodes.values():
                # Apply filters
                if status_filter and node.status.value != status_filter:
                    continue
                if type_filter and node.node_type.value != type_filter:
                    continue
                
                nodes.append(node.to_dict())
        
        return nodes
    
    def update_node(self, node_id: str, **updates) -> bool:
        """Update node properties."""
        with self._nodes_lock:
            node = self._nodes.get(node_id)
            if not node:
                return False
            
            # Update allowed properties
            for key, value in updates.items():
                if key == 'metadata' and isinstance(value, dict):
                    node.metadata.update(value)
                elif key == 'capabilities' and isinstance(value, (list, set)):
                    node.capabilities.update(set(value))
                elif key == 'status' and isinstance(value, str):
                    node.status = NodeStatus(value)
                # Don't allow updating id, name, node_type, created_at
        
        self._log_communication("NODE_UPDATED", {
            "node_id": node_id,
            "updates": list(updates.keys())
        })
        
        return True
    
    def remove_node(self, node_id: str) -> bool:
        """Remove a node from the SeedGrid."""
        with self._nodes_lock:
            if node_id in self._nodes:
                node = self._nodes.pop(node_id)
                
                self._log_communication("NODE_REMOVED", {
                    "node_id": node_id,
                    "name": node.name
                })
                
                logger.info(f"Removed node: {node.name} ({node_id})")
                return True
        
        return False
    
    def heartbeat(self, node_id: str) -> bool:
        """Record a heartbeat from a node."""
        with self._nodes_lock:
            node = self._nodes.get(node_id)
            if node:
                node.last_heartbeat = datetime.utcnow()
                if node.status == NodeStatus.FAILED:
                    node.status = NodeStatus.ACTIVE
                    logger.info(f"Node {node.name} recovered from failure")
                return True
        
        return False
    
    def send_message(self, from_node_id: str, to_node_id: str, 
                    message_type: str, payload: Dict[str, Any]) -> bool:
        """Send a message between nodes."""
        with self._nodes_lock:
            from_node = self._nodes.get(from_node_id)
            to_node = self._nodes.get(to_node_id)
            
            if not from_node or not to_node:
                return False
            
            if from_node.status != NodeStatus.ACTIVE or to_node.status != NodeStatus.ACTIVE:
                return False
        
        self._log_communication("MESSAGE_SENT", {
            "from_node": from_node_id,
            "to_node": to_node_id,
            "message_type": message_type,
            "payload_size": len(str(payload))
        })
        
        # In a real implementation, this would actually deliver the message
        # For now, we just log it
        logger.debug(f"Message {message_type} sent from {from_node_id} to {to_node_id}")
        return True
    
    def broadcast_message(self, from_node_id: str, message_type: str, 
                         payload: Dict[str, Any], node_type_filter: Optional[str] = None) -> int:
        """Broadcast a message to multiple nodes."""
        sent_count = 0
        
        with self._nodes_lock:
            from_node = self._nodes.get(from_node_id)
            if not from_node or from_node.status != NodeStatus.ACTIVE:
                return 0
            
            for node_id, node in self._nodes.items():
                if node_id == from_node_id:
                    continue
                
                if node.status != NodeStatus.ACTIVE:
                    continue
                
                if node_type_filter and node.node_type.value != node_type_filter:
                    continue
                
                # Send message
                if self.send_message(from_node_id, node_id, message_type, payload):
                    sent_count += 1
        
        self._log_communication("MESSAGE_BROADCAST", {
            "from_node": from_node_id,
            "message_type": message_type,
            "recipients": sent_count
        })
        
        return sent_count
    
    def _start_heartbeat_monitoring(self) -> None:
        """Start the heartbeat monitoring thread."""
        def monitor_heartbeats():
            while not self._heartbeat_stop_event.wait(self.heartbeat_interval):
                self._check_node_health()
        
        self._heartbeat_thread = Thread(target=monitor_heartbeats, daemon=True)
        self._heartbeat_thread.start()
        logger.info("Heartbeat monitoring started")
    
    def _check_node_health(self) -> None:
        """Check the health of all nodes based on heartbeats."""
        now = datetime.utcnow()
        timeout_threshold = self.heartbeat_interval * 3  # Allow 3 missed heartbeats
        
        failed_nodes = []
        
        with self._nodes_lock:
            for node in self._nodes.values():
                if node.status == NodeStatus.ACTIVE:
                    time_since_heartbeat = (now - node.last_heartbeat).total_seconds()
                    
                    if time_since_heartbeat > timeout_threshold:
                        node.status = NodeStatus.FAILED
                        failed_nodes.append(node)
        
        # Log failed nodes
        for node in failed_nodes:
            logger.warning(f"Node {node.name} ({node.id}) marked as failed - no heartbeat for {time_since_heartbeat:.1f}s")
    
    def _log_communication(self, event_type: str, data: Dict[str, Any]) -> None:
        """Log communication events."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "data": data
        }
        
        self._communication_log.append(log_entry)
        
        # Keep log size manageable
        if len(self._communication_log) > 1000:
            self._communication_log = self._communication_log[-500:]
    
    def get_communication_log(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get communication log entries."""
        if limit:
            return self._communication_log[-limit:]
        return self._communication_log.copy()
    
    def get_status(self) -> Dict[str, Any]:
        """Get SeedGrid status."""
        with self._nodes_lock:
            node_counts = {}
            for status in NodeStatus:
                node_counts[status.value] = sum(1 for node in self._nodes.values() if node.status == status)
        
        return {
            'initialized': self.initialized,
            'total_nodes': len(self._nodes),
            'node_counts_by_status': node_counts,
            'heartbeat_interval': self.heartbeat_interval,
            'communication_log_size': len(self._communication_log)
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Run health check on SeedGrid."""
        issues = []
        
        if not self.initialized:
            issues.append("SeedGrid not initialized")
        
        if not self._heartbeat_thread or not self._heartbeat_thread.is_alive():
            issues.append("Heartbeat monitoring not running")
        
        with self._nodes_lock:
            failed_nodes = sum(1 for node in self._nodes.values() if node.status == NodeStatus.FAILED)
            if failed_nodes > 0:
                issues.append(f"{failed_nodes} nodes are in failed state")
        
        return {
            'healthy': len(issues) == 0,
            'issues': issues,
            'status': self.get_status()
        }