"""RECURSIVE_FAILURE_PROBE component module."""
from __future__ import annotations

from ..blueprint import create_component


def RECURSIVE_FAILURE_PROBE() -> dict[str, object]:
    """Return the RECURSIVE_FAILURE_PROBE component description."""
    return create_component(
        "RECURSIVE_FAILURE_PROBE",
        "sandbox",
    )
