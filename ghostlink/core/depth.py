"""DEPTH component module."""
from __future__ import annotations

from ..blueprint import create_component


def DEPTH() -> dict[str, object]:
    """Return the DEPTH component description."""
    return create_component(
        "DEPTH",
        "core",
    )
