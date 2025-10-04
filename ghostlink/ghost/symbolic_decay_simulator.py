"""SYMBOLIC_DECAY_SIMULATOR component module."""
from __future__ import annotations

from ..blueprint import create_component


def SYMBOLIC_DECAY_SIMULATOR() -> dict[str, object]:
    """Return the SYMBOLIC_DECAY_SIMULATOR component description."""
    return create_component(
        "SYMBOLIC_DECAY_SIMULATOR",
        "ghost",
    )
