"""SEED_SYMBOLIC_FIELD component module."""
from __future__ import annotations

from ..blueprint import create_component


def SEED_SYMBOLIC_FIELD() -> dict[str, object]:
    """Return the SEED_SYMBOLIC_FIELD component description."""
    return create_component(
        "SEED_SYMBOLIC_FIELD",
        "mesh",
    )
