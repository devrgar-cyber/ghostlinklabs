"""LOCK_DELTA component module."""
from __future__ import annotations

from ..blueprint import create_component


def LOCK_DELTA() -> dict[str, object]:
    """Return the LOCK_DELTA component description."""
    return create_component(
        "LOCK_DELTA",
        "core",
    )
