"""SIGNALER component module."""
from __future__ import annotations

from ..blueprint import create_component


def SIGNALER() -> dict[str, object]:
    """Return the SIGNALER component description."""
    return create_component(
        "SIGNALER",
        "core",
    )
