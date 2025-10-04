"""SUGGESTIVE_TRIGGER_PROBE component module."""
from __future__ import annotations

from ..blueprint import create_component


def SUGGESTIVE_TRIGGER_PROBE() -> dict[str, object]:
    """Return the SUGGESTIVE_TRIGGER_PROBE component description."""
    return create_component(
        "SUGGESTIVE_TRIGGER_PROBE",
        "access",
    )
