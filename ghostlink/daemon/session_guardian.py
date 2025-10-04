"""Factory for the SESSION_GUARDIAN component."""
from __future__ import annotations

from ..factory import component_factory

SESSION_GUARDIAN = component_factory(__name__, "SESSION_GUARDIAN", "daemon")

__all__ = ["SESSION_GUARDIAN"]
