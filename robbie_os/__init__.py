"""
Robbie OS - A Sovereign Operating System Framework
Based on ClarityOS concepts and principles

Core Components:
- ClarityOS: Main OS engine
- SeedGrid: Node management and communication
- Sentinel: Oversight and ethical enforcement
- Memory: Persistent state management
- Failure Detection: Anomaly detection and learning
"""

from .core import RobbieOS
from .seedgrid import SeedGrid, SeedNode
from .sentinel import Sentinel
from .memory import MemoryEngine
from .failure_detector import FailureDetector

__version__ = "1.0.0"
__all__ = ["RobbieOS", "SeedGrid", "SeedNode", "Sentinel", "MemoryEngine", "FailureDetector"]