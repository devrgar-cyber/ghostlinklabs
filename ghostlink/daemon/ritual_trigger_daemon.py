"""Factory for the RITUAL_TRIGGER_DAEMON component."""
from __future__ import annotations

from ..factory import component_factory

RITUAL_TRIGGER_DAEMON = component_factory(__name__, "RITUAL_TRIGGER_DAEMON", "daemon")

__all__ = ["RITUAL_TRIGGER_DAEMON"]
