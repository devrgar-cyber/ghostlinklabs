"""Factory for the RECURSIVE_FAULT_MATCHER component."""
from __future__ import annotations

from ..factory import component_factory

RECURSIVE_FAULT_MATCHER = component_factory(__name__, "RECURSIVE_FAULT_MATCHER", "diagnostic")

__all__ = ["RECURSIVE_FAULT_MATCHER"]
