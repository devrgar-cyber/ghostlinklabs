"""ECHO_MONITOR_DAEMON component module."""
from __future__ import annotations

from ..blueprint import create_component


def ECHO_MONITOR_DAEMON() -> dict[str, object]:
    """Return the ECHO_MONITOR_DAEMON component description."""
    return create_component(
        "ECHO_MONITOR_DAEMON",
        "daemon",
    )
