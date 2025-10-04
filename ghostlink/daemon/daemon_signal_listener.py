"""Factory for the DAEMON_SIGNAL_LISTENER component."""
from __future__ import annotations

from ..factory import component_factory

DAEMON_SIGNAL_LISTENER = component_factory(__name__, "DAEMON_SIGNAL_LISTENER", "daemon")

__all__ = ["DAEMON_SIGNAL_LISTENER"]
