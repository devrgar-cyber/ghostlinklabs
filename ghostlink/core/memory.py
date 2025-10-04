"""MEMORY component module."""
from __future__ import annotations

from ..blueprint import create_component


def MEMORY() -> dict[str, object]:
    """Return the MEMORY component description."""
    return create_component(
        "MEMORY",
        "core",
    )
