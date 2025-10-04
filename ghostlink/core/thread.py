"""THREAD component module."""
from __future__ import annotations

from ..blueprint import create_component


def THREAD() -> dict[str, object]:
    """Return the THREAD component description."""
    return create_component(
        "THREAD",
        "core",
    )
