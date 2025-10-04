"""SURFACE component module."""
from __future__ import annotations

from ..blueprint import create_component


def SURFACE() -> dict[str, object]:
    """Return the SURFACE component description."""
    return create_component(
        "SURFACE",
        "core",
    )
