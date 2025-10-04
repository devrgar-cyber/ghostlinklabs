"""GRID component module."""
from __future__ import annotations

from ..blueprint import create_component


def GRID() -> dict[str, object]:
    """Return the GRID component description."""
    return create_component(
        "GRID",
        "core",
    )
