"""Factory for the RUNTIME_STATE_MANAGER component."""
from __future__ import annotations

from ..factory import component_factory

RUNTIME_STATE_MANAGER = component_factory(__name__, "RUNTIME_STATE_MANAGER", "runtime")

__all__ = ["RUNTIME_STATE_MANAGER"]
