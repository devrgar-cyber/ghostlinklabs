"""TOOL_FORGE component module."""
from __future__ import annotations

from ..blueprint import create_component


def TOOL_FORGE() -> dict[str, object]:
    """Return the TOOL_FORGE component description."""
    return create_component(
        "TOOL_FORGE",
        "forge",
    )
