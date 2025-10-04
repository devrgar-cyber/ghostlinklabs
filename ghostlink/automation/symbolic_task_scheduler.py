"""Factory for the SYMBOLIC_TASK_SCHEDULER component."""
from __future__ import annotations

from ..factory import component_factory

SYMBOLIC_TASK_SCHEDULER = component_factory(__name__, "SYMBOLIC_TASK_SCHEDULER", "automation")

__all__ = ["SYMBOLIC_TASK_SCHEDULER"]
