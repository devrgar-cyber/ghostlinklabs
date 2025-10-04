"""OVERCOMPRESSION_RESOLVER component module."""
from __future__ import annotations

from ..blueprint import create_component


def OVERCOMPRESSION_RESOLVER() -> dict[str, object]:
    """Return the OVERCOMPRESSION_RESOLVER component description."""
    return create_component(
        "OVERCOMPRESSION_RESOLVER",
        "reflect",
    )
