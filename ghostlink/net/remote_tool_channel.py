"""REMOTE_TOOL_CHANNEL component module."""
from __future__ import annotations

from ..blueprint import create_component


def REMOTE_TOOL_CHANNEL() -> dict[str, object]:
    """Return the REMOTE_TOOL_CHANNEL component description."""
    return create_component(
        "REMOTE_TOOL_CHANNEL",
        "net",
    )
