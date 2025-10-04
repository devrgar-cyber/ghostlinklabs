"""MIRROR_SHEAR component module."""
from __future__ import annotations

from ..blueprint import create_component


def MIRROR_SHEAR() -> dict[str, object]:
    """Return the MIRROR_SHEAR component description."""
    return create_component(
        "MIRROR_SHEAR",
        "core",
    )
