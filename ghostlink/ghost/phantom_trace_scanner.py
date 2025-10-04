"""PHANTOM_TRACE_SCANNER component module."""
from __future__ import annotations

from ..blueprint import create_component


def PHANTOM_TRACE_SCANNER() -> dict[str, object]:
    """Return the PHANTOM_TRACE_SCANNER component description."""
    return create_component(
        "PHANTOM_TRACE_SCANNER",
        "ghost",
    )
