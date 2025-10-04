"""GHOST component module."""
from __future__ import annotations

from ..blueprint import create_component


def GHOST() -> dict[str, object]:
    """Return the GHOST component description."""
    return create_component(
        "GHOST",
        "core",
    )
