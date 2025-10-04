"""Factory for the AVOIDANCE_PATTERN_MAP component."""
from __future__ import annotations

from ..factory import component_factory

AVOIDANCE_PATTERN_MAP = component_factory(__name__, "AVOIDANCE_PATTERN_MAP", "diagnostic")

__all__ = ["AVOIDANCE_PATTERN_MAP"]
