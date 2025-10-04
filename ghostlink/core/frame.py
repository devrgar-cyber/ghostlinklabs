"""FRAME component module."""
from __future__ import annotations

from ..blueprint import create_component


def FRAME() -> dict[str, object]:
    """Return the FRAME component description."""
    return create_component(
        "FRAME",
        "core",
    )
