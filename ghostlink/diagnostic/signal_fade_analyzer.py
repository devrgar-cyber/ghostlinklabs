"""SIGNAL_FADE_ANALYZER component module."""
from __future__ import annotations

from ..blueprint import create_component


def SIGNAL_FADE_ANALYZER() -> dict[str, object]:
    """Return the SIGNAL_FADE_ANALYZER component description."""
    return create_component(
        "SIGNAL_FADE_ANALYZER",
        "diagnostic",
    )
