"""SYMPTOM_MASK_DETECTOR component module."""
from __future__ import annotations

from ..blueprint import create_component


def SYMPTOM_MASK_DETECTOR() -> dict[str, object]:
    """Return the SYMPTOM_MASK_DETECTOR component description."""
    return create_component(
        "SYMPTOM_MASK_DETECTOR",
        "diagnostic",
    )
