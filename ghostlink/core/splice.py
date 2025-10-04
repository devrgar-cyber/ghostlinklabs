"""SPLICE component module."""
from __future__ import annotations

from ..blueprint import create_component


def SPLICE() -> dict[str, object]:
    """Return the SPLICE component description."""
    return create_component(
        "SPLICE",
        "core",
    )
