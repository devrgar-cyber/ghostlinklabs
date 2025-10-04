"""CALM component module."""
from __future__ import annotations

from ..blueprint import create_component


def CALM() -> dict[str, object]:
    """Return the CALM component description."""
    return create_component(
        "CALM",
        "core",
    )
