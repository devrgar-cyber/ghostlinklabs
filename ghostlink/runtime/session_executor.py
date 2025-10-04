"""Factory for the SESSION_EXECUTOR component."""
from __future__ import annotations

from ..factory import component_factory

SESSION_EXECUTOR = component_factory(__name__, "SESSION_EXECUTOR", "runtime")

__all__ = ["SESSION_EXECUTOR"]
