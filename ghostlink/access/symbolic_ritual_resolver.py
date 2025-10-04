"""SYMBOLIC_RITUAL_RESOLVER component module."""
from __future__ import annotations

from ..blueprint import create_component


def SYMBOLIC_RITUAL_RESOLVER() -> dict[str, object]:
    """Return the SYMBOLIC_RITUAL_RESOLVER component description."""
    return create_component(
        "SYMBOLIC_RITUAL_RESOLVER",
        "access",
    )
