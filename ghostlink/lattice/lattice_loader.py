"""LOAD_LATTICE component module."""
from __future__ import annotations

from ..blueprint import create_component


def LOAD_LATTICE() -> dict[str, object]:
    """Return the LOAD_LATTICE component description."""
    return create_component(
        "LOAD_LATTICE",
        "lattice",
    )
