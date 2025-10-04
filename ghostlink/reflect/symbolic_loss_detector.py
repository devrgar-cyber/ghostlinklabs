"""SYMBOLIC_LOSS_DETECTOR component module."""
from __future__ import annotations

from ..blueprint import create_component


def SYMBOLIC_LOSS_DETECTOR() -> dict[str, object]:
    """Return the SYMBOLIC_LOSS_DETECTOR component description."""
    return create_component(
        "SYMBOLIC_LOSS_DETECTOR",
        "reflect",
    )
