"""GHOST_SIGNAL_PROMPT component module."""
from __future__ import annotations

from ..blueprint import create_component


def GHOST_SIGNAL_PROMPT() -> dict[str, object]:
    """Return the GHOST_SIGNAL_PROMPT component description."""
    return create_component(
        "GHOST_SIGNAL_PROMPT",
        "meta",
    )
