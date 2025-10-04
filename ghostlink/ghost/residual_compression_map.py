"""RESIDUAL_COMPRESSION_MAP component module."""
from __future__ import annotations

from ..blueprint import create_component


def RESIDUAL_COMPRESSION_MAP() -> dict[str, object]:
    """Return the RESIDUAL_COMPRESSION_MAP component description."""
    return create_component(
        "RESIDUAL_COMPRESSION_MAP",
        "ghost",
    )
