"""PULSE component module."""
from __future__ import annotations

from ..blueprint import create_component


def PULSE() -> dict[str, object]:
    """Return the PULSE component description."""
    return create_component(
        "PULSE",
        "core",
    )
