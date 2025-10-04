"""SIGNAL_CASCADE_CHECK component module."""
from __future__ import annotations

from ..blueprint import create_component


def SIGNAL_CASCADE_CHECK() -> dict[str, object]:
    """Return the SIGNAL_CASCADE_CHECK component description."""
    return create_component(
        "SIGNAL_CASCADE_CHECK",
        "diagnostic",
    )
