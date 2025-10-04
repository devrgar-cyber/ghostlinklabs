"""SYMBOLIC_SANDBOX component module."""
from __future__ import annotations

from ..blueprint import create_component


def SYMBOLIC_SANDBOX() -> dict[str, object]:
    """Return the SYMBOLIC_SANDBOX component description."""
    return create_component(
        "SYMBOLIC_SANDBOX",
        "sandbox",
    )
