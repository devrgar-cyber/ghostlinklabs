"""Factory for the ECHO_MONITOR_DAEMON component."""
from __future__ import annotations

from ..factory import component_factory

ECHO_MONITOR_DAEMON = component_factory(__name__, "ECHO_MONITOR_DAEMON", "daemon")

__all__ = ["ECHO_MONITOR_DAEMON"]
