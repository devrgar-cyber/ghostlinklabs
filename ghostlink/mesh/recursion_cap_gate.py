"""RECURSION_CAP_GATE component module."""
from __future__ import annotations

from ..blueprint import create_component


def RECURSION_CAP_GATE() -> dict[str, object]:
    """Return the RECURSION_CAP_GATE component description."""
    return create_component(
        "RECURSION_CAP_GATE",
        "mesh",
    )
