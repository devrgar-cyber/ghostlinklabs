"""TILE component module."""
from __future__ import annotations

from ..blueprint import create_component


def TILE() -> dict[str, object]:
    """Return the TILE component description."""
    return create_component(
        "TILE",
        "core",
    )
