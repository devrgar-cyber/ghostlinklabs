"""RITUAL_LOOP_PROMPT component module."""
from __future__ import annotations

from ..blueprint import create_component


def RITUAL_LOOP_PROMPT() -> dict[str, object]:
    """Return the RITUAL_LOOP_PROMPT component description."""
    return create_component(
        "RITUAL_LOOP_PROMPT",
        "meta",
    )
