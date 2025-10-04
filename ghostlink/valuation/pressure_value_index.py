"""Factory for the PRESSURE_VALUE_INDEX component."""
from __future__ import annotations

from ..factory import component_factory

PRESSURE_VALUE_INDEX = component_factory(__name__, "PRESSURE_VALUE_INDEX", "valuation")

__all__ = ["PRESSURE_VALUE_INDEX"]
