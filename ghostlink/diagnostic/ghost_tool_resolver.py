"""GHOST_TOOL_RESOLVER component module."""
from __future__ import annotations

from ..blueprint import create_component


def GHOST_TOOL_RESOLVER() -> dict[str, object]:
    """Return the GHOST_TOOL_RESOLVER component description."""
    return create_component(
        "GHOST_TOOL_RESOLVER",
        "diagnostic",
    )
