"""REFLECTIVE_MIRROR component module."""
from __future__ import annotations

from ..blueprint import create_component


def REFLECTIVE_MIRROR() -> dict[str, object]:
    """Return the REFLECTIVE_MIRROR component description."""
    return create_component(
        "REFLECTIVE_MIRROR",
        "reflect",
    )
