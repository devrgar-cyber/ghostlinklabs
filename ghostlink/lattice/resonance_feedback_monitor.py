"""RESONANCE_FEEDBACK_MONITOR component module."""
from __future__ import annotations

from ..blueprint import create_component


def RESONANCE_FEEDBACK_MONITOR() -> dict[str, object]:
    """Return the RESONANCE_FEEDBACK_MONITOR component description."""
    return create_component(
        "RESONANCE_FEEDBACK_MONITOR",
        "lattice",
    )
