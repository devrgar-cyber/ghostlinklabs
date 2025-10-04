"""GATE component module."""
from __future__ import annotations

from ..blueprint import create_component


def GATE() -> dict[str, object]:
    """Return the GATE component description."""
    return create_component(
        "GATE",
        "core",
    )
