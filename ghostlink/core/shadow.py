"""SHADOW component module."""
from __future__ import annotations

from ..blueprint import create_component


def SHADOW() -> dict[str, object]:
    """Return the SHADOW component description."""
    return create_component(
        "SHADOW",
        "core",
    )
