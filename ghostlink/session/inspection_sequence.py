"""INSPECTION_SEQUENCE component module."""
from __future__ import annotations

from ..blueprint import create_component


def INSPECTION_SEQUENCE() -> dict[str, object]:
    """Return the INSPECTION_SEQUENCE component description."""
    return create_component(
        "INSPECTION_SEQUENCE",
        "session",
    )
