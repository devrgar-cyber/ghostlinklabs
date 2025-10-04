"""FORGE component module."""
from __future__ import annotations

from ..blueprint import create_component


def FORGE() -> dict[str, object]:
    """Return the FORGE component description."""
    return create_component(
        "FORGE",
        "core",
    )
