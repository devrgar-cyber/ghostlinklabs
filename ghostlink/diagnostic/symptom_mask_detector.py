"""SYMPTOM_MASK_DETECTOR component module."""
from __future__ import annotations

from ..blueprint import component_factory


SYMPTOM_MASK_DETECTOR = component_factory("SYMPTOM_MASK_DETECTOR", "diagnostic", module=__name__)
