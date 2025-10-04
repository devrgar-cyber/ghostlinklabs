"""Factory for the SESSION_TRACKER component."""
from __future__ import annotations

from ..factory import component_factory

SESSION_TRACKER = component_factory(__name__, "SESSION_TRACKER", "session")

__all__ = ["SESSION_TRACKER"]
