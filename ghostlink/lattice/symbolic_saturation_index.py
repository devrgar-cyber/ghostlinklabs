"""SYMBOLIC_SATURATION_INDEX component module."""
from __future__ import annotations

from ..blueprint import create_component


def SYMBOLIC_SATURATION_INDEX() -> dict[str, object]:
    """Return the SYMBOLIC_SATURATION_INDEX component description."""
    return create_component(
        "SYMBOLIC_SATURATION_INDEX",
        "lattice",
    )
