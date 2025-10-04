"""GHOST_PATH_VALIDATOR component module."""
from __future__ import annotations

from ..blueprint import create_component


def GHOST_PATH_VALIDATOR() -> dict[str, object]:
    """Return the GHOST_PATH_VALIDATOR component description."""
    return create_component(
        "GHOST_PATH_VALIDATOR",
        "test",
    )
