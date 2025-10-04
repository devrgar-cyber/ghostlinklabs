"""RITUAL_UNLOCK component module."""
from __future__ import annotations

from ..blueprint import create_component


def RITUAL_UNLOCK() -> dict[str, object]:
    """Return the RITUAL_UNLOCK component description."""
    return create_component(
        "RITUAL_UNLOCK",
        "access",
    )
