"""LIVE_TOOL_ROUTER component module."""
from __future__ import annotations

from ..blueprint import create_component


def LIVE_TOOL_ROUTER() -> dict[str, object]:
    """Return the LIVE_TOOL_ROUTER component description."""
    return create_component(
        "LIVE_TOOL_ROUTER",
        "runtime",
    )
