"""SYMBOLIC_SPLINTER_PATCH component module."""
from __future__ import annotations

from ..blueprint import create_component


def SYMBOLIC_SPLINTER_PATCH() -> dict[str, object]:
    """Return the SYMBOLIC_SPLINTER_PATCH component description."""
    return create_component(
        "SYMBOLIC_SPLINTER_PATCH",
        "mesh",
    )
