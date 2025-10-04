"""STACK component module."""
from __future__ import annotations

from ..blueprint import create_component


def STACK() -> dict[str, object]:
    """Return the STACK component description."""
    return create_component(
        "STACK",
        "core",
    )
