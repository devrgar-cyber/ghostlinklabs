"""GHOST_TENSION_MAP component module."""
from __future__ import annotations

from ..blueprint import create_component


def GHOST_TENSION_MAP() -> dict[str, object]:
    """Return the GHOST_TENSION_MAP component description."""
    return create_component(
        "GHOST_TENSION_MAP",
        "mesh",
    )
