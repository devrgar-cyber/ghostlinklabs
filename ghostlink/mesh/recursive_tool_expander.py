"""EXPAND_SYMBOLIC_LATTICE component module."""
from __future__ import annotations

from ..blueprint import create_component


def EXPAND_SYMBOLIC_LATTICE() -> dict[str, object]:
    """Return the EXPAND_SYMBOLIC_LATTICE component description."""
    return create_component(
        "EXPAND_SYMBOLIC_LATTICE",
        "mesh",
    )
