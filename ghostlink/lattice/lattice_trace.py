"""TRACE_LATTICE_PATH component module."""
from __future__ import annotations

from ..blueprint import create_component


def TRACE_LATTICE_PATH() -> dict[str, object]:
    """Return the TRACE_LATTICE_PATH component description."""
    return create_component(
        "TRACE_LATTICE_PATH",
        "lattice",
    )
