"""RESONANCE component module."""
from __future__ import annotations

from ..blueprint import create_component


def RESONANCE() -> dict[str, object]:
    """Return the RESONANCE component description."""
    return create_component(
        "RESONANCE",
        "core",
    )
