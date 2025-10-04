"""RUNTIME_STATE_MANAGER component module."""
from __future__ import annotations

from ..blueprint import create_component


def RUNTIME_STATE_MANAGER() -> dict[str, object]:
    """Return the RUNTIME_STATE_MANAGER component description."""
    return create_component(
        "RUNTIME_STATE_MANAGER",
        "runtime",
    )
