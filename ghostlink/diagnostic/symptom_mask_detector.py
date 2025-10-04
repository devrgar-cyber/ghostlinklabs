"""Factory for the SYMPTOM_MASK_DETECTOR component."""
from __future__ import annotations

from ..factory import component_factory

SYMPTOM_MASK_DETECTOR = component_factory(__name__, "SYMPTOM_MASK_DETECTOR", "diagnostic")

__all__ = ["SYMPTOM_MASK_DETECTOR"]
