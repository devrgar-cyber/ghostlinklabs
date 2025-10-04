"""DISSOLUTION_THRESHOLD_PROBE component module."""
from __future__ import annotations

from ..blueprint import create_component


def DISSOLUTION_THRESHOLD_PROBE() -> dict[str, object]:
    """Return the DISSOLUTION_THRESHOLD_PROBE component description."""
    return create_component(
        "DISSOLUTION_THRESHOLD_PROBE",
        "observer",
    )
