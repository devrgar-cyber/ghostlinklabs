"""MIRROR component module."""
from __future__ import annotations

from ..blueprint import create_component


def MIRROR() -> dict[str, object]:
    """Return the MIRROR component description."""
    return create_component(
        "MIRROR",
        "core",
    )
