"""NETWORK_SIGNAL_MIRROR component module."""
from __future__ import annotations

from ..blueprint import create_component


def NETWORK_SIGNAL_MIRROR() -> dict[str, object]:
    """Return the NETWORK_SIGNAL_MIRROR component description."""
    return create_component(
        "NETWORK_SIGNAL_MIRROR",
        "net",
    )
