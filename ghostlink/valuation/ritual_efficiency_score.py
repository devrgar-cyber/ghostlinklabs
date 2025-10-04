"""RITUAL_EFFICIENCY_SCORE component module."""
from __future__ import annotations

from ..blueprint import create_component


def RITUAL_EFFICIENCY_SCORE() -> dict[str, object]:
    """Return the RITUAL_EFFICIENCY_SCORE component description."""
    return create_component(
        "RITUAL_EFFICIENCY_SCORE",
        "valuation",
    )
