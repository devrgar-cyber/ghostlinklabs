"""THRESHOLD component module."""
from __future__ import annotations

from ..blueprint import create_component


def THRESHOLD() -> dict[str, object]:
    """Return the THRESHOLD component description."""
    return create_component(
        "THRESHOLD",
        "core",
    )
