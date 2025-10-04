"""STATIC component module."""
from __future__ import annotations

from ..blueprint import create_component


def STATIC() -> dict[str, object]:
    """Return the STATIC component description."""
    return create_component(
        "STATIC",
        "core",
    )
