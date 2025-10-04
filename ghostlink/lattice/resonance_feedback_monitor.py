"""Factory for the RESONANCE_FEEDBACK_MONITOR component."""
from __future__ import annotations

from ..factory import component_factory

RESONANCE_FEEDBACK_MONITOR = component_factory(__name__, "RESONANCE_FEEDBACK_MONITOR", "lattice")

__all__ = ["RESONANCE_FEEDBACK_MONITOR"]
