"""ECHO_MONITOR_DAEMON component module."""
from __future__ import annotations

from ..blueprint import component_factory


ECHO_MONITOR_DAEMON = component_factory("ECHO_MONITOR_DAEMON", "daemon", module=__name__)
