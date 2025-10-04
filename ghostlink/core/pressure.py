"""PRESSURE component module."""
from __future__ import annotations

from ..blueprint import create_component


def PRESSURE() -> dict[str, object]:
    """Return the PRESSURE component description."""
    return create_component(
        "PRESSURE",
        "core",
    )
