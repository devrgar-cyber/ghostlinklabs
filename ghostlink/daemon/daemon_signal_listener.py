"""DAEMON_SIGNAL_LISTENER component module."""
from __future__ import annotations

from ..blueprint import component_factory


DAEMON_SIGNAL_LISTENER = component_factory("DAEMON_SIGNAL_LISTENER", "daemon", module=__name__)
