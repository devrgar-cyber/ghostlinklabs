"""MEMORY_REGISTER component module."""
from __future__ import annotations

from ..blueprint import create_component


def MEMORY_REGISTER() -> dict[str, object]:
    """Return the MEMORY_REGISTER component description."""
    return create_component(
        "MEMORY_REGISTER",
        "runtime",
    )
