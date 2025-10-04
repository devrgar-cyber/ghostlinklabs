"""ALIGNMENT_VECTOR_PROBE component module."""
from __future__ import annotations

from ..blueprint import create_component


def ALIGNMENT_VECTOR_PROBE() -> dict[str, object]:
    """Return the ALIGNMENT_VECTOR_PROBE component description."""
    return create_component(
        "ALIGNMENT_VECTOR_PROBE",
        "lattice",
    )
