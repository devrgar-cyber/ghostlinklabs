"""RITUAL_LOOP_DETECTOR component module."""
from __future__ import annotations

from ..blueprint import create_component


def RITUAL_LOOP_DETECTOR() -> dict[str, object]:
    """Return the RITUAL_LOOP_DETECTOR component description."""
    return create_component(
        "RITUAL_LOOP_DETECTOR",
        "diagnostic",
    )
