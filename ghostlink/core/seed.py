"""SEED component module."""
from __future__ import annotations

from ..blueprint import create_component


def SEED() -> dict[str, object]:
    """Return the SEED component description."""
    return create_component(
        "SEED",
        "core",
    )
