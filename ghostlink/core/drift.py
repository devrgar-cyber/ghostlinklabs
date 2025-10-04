"""DRIFT component module."""
from __future__ import annotations

from ..blueprint import create_component


def DRIFT() -> dict[str, object]:
    """Return the DRIFT component description."""
    return create_component(
        "DRIFT",
        "core",
    )
