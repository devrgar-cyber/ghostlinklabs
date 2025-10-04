"""SYMBOLIC_ALLOY component module."""
from __future__ import annotations

from ..blueprint import create_component


def SYMBOLIC_ALLOY() -> dict[str, object]:
    """Return the SYMBOLIC_ALLOY component description."""
    return create_component(
        "SYMBOLIC_ALLOY",
        "forge",
    )
