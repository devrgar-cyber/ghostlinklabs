"""SYMBOLIC_RITUAL_CLASSIFIER component module."""
from __future__ import annotations

from ..blueprint import create_component


def SYMBOLIC_RITUAL_CLASSIFIER() -> dict[str, object]:
    """Return the SYMBOLIC_RITUAL_CLASSIFIER component description."""
    return create_component(
        "SYMBOLIC_RITUAL_CLASSIFIER",
        "diagnostic",
    )
