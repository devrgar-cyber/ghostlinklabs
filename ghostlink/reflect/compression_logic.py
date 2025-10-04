"""COMPRESSION_LOGIC component module."""
from __future__ import annotations

from ..blueprint import create_component


def COMPRESSION_LOGIC() -> dict[str, object]:
    """Return the COMPRESSION_LOGIC component description."""
    return create_component(
        "COMPRESSION_LOGIC",
        "reflect",
    )
