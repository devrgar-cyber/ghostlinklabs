"""MARKER component module."""
from __future__ import annotations

from ..blueprint import create_component


def MARKER() -> dict[str, object]:
    """Return the MARKER component description."""
    return create_component(
        "MARKER",
        "core",
    )
