"""RITUAL_TRIGGER_DAEMON component module."""
from __future__ import annotations

from ..blueprint import component_factory


RITUAL_TRIGGER_DAEMON = component_factory("RITUAL_TRIGGER_DAEMON", "daemon", module=__name__)
