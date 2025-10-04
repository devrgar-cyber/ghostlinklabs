"""Factory for the FRACTURE_HEARTBEAT component."""
from __future__ import annotations

from ..factory import component_factory

FRACTURE_HEARTBEAT = component_factory(__name__, "FRACTURE_HEARTBEAT", "daemon")

__all__ = ["FRACTURE_HEARTBEAT"]
