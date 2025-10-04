"""LIVE_SIGNAL_RENDERER component module."""
from __future__ import annotations

from ..blueprint import create_component


def LIVE_SIGNAL_RENDERER() -> dict[str, object]:
    """Return the LIVE_SIGNAL_RENDERER component description."""
    return create_component(
        "LIVE_SIGNAL_RENDERER",
        "gui",
    )
