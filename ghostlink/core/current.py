"""CURRENT component module."""
from __future__ import annotations

from ..blueprint import create_component


def CURRENT() -> dict[str, object]:
    """Return the CURRENT component description."""
    return create_component(
        "CURRENT",
        "core",
    )
