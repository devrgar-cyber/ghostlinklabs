"""SYMBOLIC_PROTOCOL_ROUTER component module."""
from __future__ import annotations

from ..blueprint import create_component


def SYMBOLIC_PROTOCOL_ROUTER() -> dict[str, object]:
    """Return the SYMBOLIC_PROTOCOL_ROUTER component description."""
    return create_component(
        "SYMBOLIC_PROTOCOL_ROUTER",
        "net",
    )
