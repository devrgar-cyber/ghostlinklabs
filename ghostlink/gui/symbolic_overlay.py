"""SYMBOLIC_OVERLAY component module."""
from __future__ import annotations

from ..blueprint import create_component


def SYMBOLIC_OVERLAY() -> dict[str, object]:
    """Return the SYMBOLIC_OVERLAY component description."""
    return create_component(
        "SYMBOLIC_OVERLAY",
        "gui",
    )
