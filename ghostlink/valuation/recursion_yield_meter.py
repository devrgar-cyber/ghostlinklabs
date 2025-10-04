"""RECURSION_YIELD_METER component module."""
from __future__ import annotations

from ..blueprint import create_component


def RECURSION_YIELD_METER() -> dict[str, object]:
    """Return the RECURSION_YIELD_METER component description."""
    return create_component(
        "RECURSION_YIELD_METER",
        "valuation",
    )
