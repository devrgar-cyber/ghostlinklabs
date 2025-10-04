"""SIGNAL component module."""
from __future__ import annotations

from ..blueprint import create_component


def SIGNAL() -> dict[str, object]:
    """Return the SIGNAL component description."""
    return create_component(
        "SIGNAL",
        "core",
    )
