"""Factory for the AUTONOMOUS_REPAIR_LOOP component."""
from __future__ import annotations

from ..factory import component_factory

AUTONOMOUS_REPAIR_LOOP = component_factory(__name__, "AUTONOMOUS_REPAIR_LOOP", "automation")

__all__ = ["AUTONOMOUS_REPAIR_LOOP"]
