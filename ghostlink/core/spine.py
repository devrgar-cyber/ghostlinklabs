"""SPINE component module."""
from __future__ import annotations

from ..blueprint import create_component


def SPINE() -> dict[str, object]:
    """Return the SPINE component description."""
    return create_component(
        "SPINE",
        "core",
    )
