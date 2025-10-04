"""COLD_STRUCTURE_GENERATOR component module."""
from __future__ import annotations

from ..blueprint import create_component


def COLD_STRUCTURE_GENERATOR() -> dict[str, object]:
    """Return the COLD_STRUCTURE_GENERATOR component description."""
    return create_component(
        "COLD_STRUCTURE_GENERATOR",
        "forge",
    )
