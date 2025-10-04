"""AVOIDANCE_PATTERN_MAP component module."""
from __future__ import annotations

from ..blueprint import create_component


def AVOIDANCE_PATTERN_MAP() -> dict[str, object]:
    """Return the AVOIDANCE_PATTERN_MAP component description."""
    return create_component(
        "AVOIDANCE_PATTERN_MAP",
        "diagnostic",
    )
