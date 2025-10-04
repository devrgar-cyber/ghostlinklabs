"""ECHO_BURN_RATE component module."""
from __future__ import annotations

from ..blueprint import create_component


def ECHO_BURN_RATE() -> dict[str, object]:
    """Return the ECHO_BURN_RATE component description."""
    return create_component(
        "ECHO_BURN_RATE",
        "valuation",
    )
