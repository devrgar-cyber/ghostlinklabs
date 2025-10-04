"""TUNNEL component module."""
from __future__ import annotations

from ..blueprint import create_component


def TUNNEL() -> dict[str, object]:
    """Return the TUNNEL component description."""
    return create_component(
        "TUNNEL",
        "core",
    )
