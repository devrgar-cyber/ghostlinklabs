"""Factory for the SYMBOLIC_LOSS_DETECTOR component."""
from __future__ import annotations

from ..factory import component_factory

SYMBOLIC_LOSS_DETECTOR = component_factory(__name__, "SYMBOLIC_LOSS_DETECTOR", "reflect")

__all__ = ["SYMBOLIC_LOSS_DETECTOR"]
