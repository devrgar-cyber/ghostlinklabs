"""Factory for the DISSOLUTION_THRESHOLD_PROBE component."""
from __future__ import annotations

from ..factory import component_factory

DISSOLUTION_THRESHOLD_PROBE = component_factory(__name__, "DISSOLUTION_THRESHOLD_PROBE", "observer")

__all__ = ["DISSOLUTION_THRESHOLD_PROBE"]
