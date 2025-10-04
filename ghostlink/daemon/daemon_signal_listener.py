"""DAEMON_SIGNAL_LISTENER component module."""
from __future__ import annotations

from ..blueprint import create_component


def DAEMON_SIGNAL_LISTENER() -> dict[str, object]:
    """Return the DAEMON_SIGNAL_LISTENER component description."""
    return create_component(
        "DAEMON_SIGNAL_LISTENER",
        "daemon",
    )
