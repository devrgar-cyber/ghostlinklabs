"""SENTINEL component module."""
from __future__ import annotations

from ..blueprint import create_component


def SENTINEL() -> dict[str, object]:
    """Return the SENTINEL component description."""
    return create_component(
        "SENTINEL",
        "core",
    )
