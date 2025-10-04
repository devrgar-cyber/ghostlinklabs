"""CHANNEL_ECHO component module."""
from __future__ import annotations

from ..blueprint import create_component


def CHANNEL_ECHO() -> dict[str, object]:
    """Return the CHANNEL_ECHO component description."""
    return create_component(
        "CHANNEL_ECHO",
        "core",
    )
