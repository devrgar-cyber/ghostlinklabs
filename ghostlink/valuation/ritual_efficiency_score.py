"""Factory for the RITUAL_EFFICIENCY_SCORE component."""
from __future__ import annotations

from ..factory import component_factory

RITUAL_EFFICIENCY_SCORE = component_factory(__name__, "RITUAL_EFFICIENCY_SCORE", "valuation")

__all__ = ["RITUAL_EFFICIENCY_SCORE"]
