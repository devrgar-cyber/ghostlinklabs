"""Factory for the RECURSION_YIELD_METER component."""
from __future__ import annotations

from ..factory import component_factory

RECURSION_YIELD_METER = component_factory(__name__, "RECURSION_YIELD_METER", "valuation")

__all__ = ["RECURSION_YIELD_METER"]
