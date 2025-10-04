"""WRAP component module."""
from __future__ import annotations

from ..blueprint import create_component


def WRAP() -> dict[str, object]:
    """Return the WRAP component description."""
    return create_component(
        "WRAP",
        "core",
    )
