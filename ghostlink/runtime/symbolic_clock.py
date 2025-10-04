"""SYMBOLIC_CLOCK component module."""
from __future__ import annotations

from ..blueprint import create_component


def SYMBOLIC_CLOCK() -> dict[str, object]:
    """Return the SYMBOLIC_CLOCK component description."""
    return create_component(
        "SYMBOLIC_CLOCK",
        "runtime",
    )
