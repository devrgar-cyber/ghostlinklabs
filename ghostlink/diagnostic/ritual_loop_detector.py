"""Factory for the RITUAL_LOOP_DETECTOR component."""
from __future__ import annotations

from ..factory import component_factory

RITUAL_LOOP_DETECTOR = component_factory(__name__, "RITUAL_LOOP_DETECTOR", "diagnostic")

__all__ = ["RITUAL_LOOP_DETECTOR"]
