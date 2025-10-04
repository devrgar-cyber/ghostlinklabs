"""SCAR_FIBER component module."""
from __future__ import annotations

from ..blueprint import create_component


def SCAR_FIBER() -> dict[str, object]:
    """Return the SCAR_FIBER component description."""
    return create_component(
        "SCAR_FIBER",
        "core",
    )
