"""SENTIENT_SIGNAL_BRIDGE component module."""
from __future__ import annotations

from ..blueprint import create_component


def SENTIENT_SIGNAL_BRIDGE() -> dict[str, object]:
    """Return the SENTIENT_SIGNAL_BRIDGE component description."""
    return create_component(
        "SENTIENT_SIGNAL_BRIDGE",
        "observer",
    )
