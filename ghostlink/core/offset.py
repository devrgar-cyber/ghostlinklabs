"""OFFSET component module."""
from __future__ import annotations

from ..blueprint import create_component


def OFFSET() -> dict[str, object]:
    """Return the OFFSET component description."""
    return create_component(
        "OFFSET",
        "core",
    )
