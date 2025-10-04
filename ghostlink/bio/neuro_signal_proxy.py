"""NEURO_SIGNAL_PROXY component module."""
from __future__ import annotations

from ..blueprint import create_component


def NEURO_SIGNAL_PROXY() -> dict[str, object]:
    """Return the NEURO_SIGNAL_PROXY component description."""
    return create_component(
        "NEURO_SIGNAL_PROXY",
        "bio",
    )
