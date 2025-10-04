"""Factory for the MEMORY_REGISTER component."""
from __future__ import annotations

from ..factory import component_factory

MEMORY_REGISTER = component_factory(__name__, "MEMORY_REGISTER", "runtime")

__all__ = ["MEMORY_REGISTER"]
