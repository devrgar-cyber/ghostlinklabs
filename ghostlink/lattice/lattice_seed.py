"""INIT_LATTICE_SLOT component module."""
from __future__ import annotations

from ..blueprint import create_component


def INIT_LATTICE_SLOT() -> dict[str, object]:
    """Return the INIT_LATTICE_SLOT component description."""
    return create_component(
        "INIT_LATTICE_SLOT",
        "lattice",
    )
