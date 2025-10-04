"""SWITCH component module."""
from __future__ import annotations

from ..blueprint import create_component


def SWITCH() -> dict[str, object]:
    """Return the SWITCH component description."""
    return create_component(
        "SWITCH",
        "core",
    )
