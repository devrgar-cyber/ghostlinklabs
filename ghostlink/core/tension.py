"""TENSION component module."""
from __future__ import annotations

from ..blueprint import create_component


def TENSION() -> dict[str, object]:
    """Return the TENSION component description."""
    return create_component(
        "TENSION",
        "core",
    )
