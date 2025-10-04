"""PRESSURE_VALUE_INDEX component module."""
from __future__ import annotations

from ..blueprint import create_component


def PRESSURE_VALUE_INDEX() -> dict[str, object]:
    """Return the PRESSURE_VALUE_INDEX component description."""
    return create_component(
        "PRESSURE_VALUE_INDEX",
        "valuation",
    )
