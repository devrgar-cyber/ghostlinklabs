"""MIRROR_FAULT_SPAWNER component module."""
from __future__ import annotations

from ..blueprint import create_component


def MIRROR_FAULT_SPAWNER() -> dict[str, object]:
    """Return the MIRROR_FAULT_SPAWNER component description."""
    return create_component(
        "MIRROR_FAULT_SPAWNER",
        "sandbox",
    )
