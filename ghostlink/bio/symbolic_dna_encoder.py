"""SYMBOLIC_DNA_ENCODER component module."""
from __future__ import annotations

from ..blueprint import create_component


def SYMBOLIC_DNA_ENCODER() -> dict[str, object]:
    """Return the SYMBOLIC_DNA_ENCODER component description."""
    return create_component(
        "SYMBOLIC_DNA_ENCODER",
        "bio",
    )
