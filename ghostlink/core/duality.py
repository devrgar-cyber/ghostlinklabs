"""DUALITY component module."""
from __future__ import annotations

from ..blueprint import create_component


def DUALITY() -> dict[str, object]:
    """Return the DUALITY component description."""
    return create_component(
        "DUALITY",
        "core",
    )
