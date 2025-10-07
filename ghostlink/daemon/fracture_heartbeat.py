"""FRACTURE_HEARTBEAT component module."""
from __future__ import annotations

from ..blueprint import component_factory


FRACTURE_HEARTBEAT = component_factory("FRACTURE_HEARTBEAT", "daemon", module=__name__)
