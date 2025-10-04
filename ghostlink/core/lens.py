"""LENS component module."""
from __future__ import annotations

from ..blueprint import create_component


def LENS() -> dict[str, object]:
    """Return the LENS component description."""
    return create_component(
        "LENS",
        "core",
    )
