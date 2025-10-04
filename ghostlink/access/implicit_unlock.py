"""IMPLICIT_UNLOCK component module."""
from __future__ import annotations

from ..blueprint import create_component


def IMPLICIT_UNLOCK() -> dict[str, object]:
    """Return the IMPLICIT_UNLOCK component description."""
    return create_component(
        "IMPLICIT_UNLOCK",
        "access",
    )
