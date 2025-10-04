"""RITUAL_TRIGGER_DAEMON component module."""
from __future__ import annotations

from ..blueprint import create_component


def RITUAL_TRIGGER_DAEMON() -> dict[str, object]:
    """Return the RITUAL_TRIGGER_DAEMON component description."""
    return create_component(
        "RITUAL_TRIGGER_DAEMON",
        "daemon",
    )
