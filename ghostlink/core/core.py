"""CORE component module."""
from __future__ import annotations

from ..blueprint import create_component


def CORE() -> dict[str, object]:
    """Return the CORE component description."""
    return create_component(
        "CORE",
        "core",
    )
