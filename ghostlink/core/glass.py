"""GLASS component module."""
from __future__ import annotations

from ..blueprint import create_component


def GLASS() -> dict[str, object]:
    """Return the GLASS component description."""
    return create_component(
        "GLASS",
        "core",
    )
