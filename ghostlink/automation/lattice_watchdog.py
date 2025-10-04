"""LATTICE_WATCHDOG component module."""
from __future__ import annotations

from ..blueprint import create_component


def LATTICE_WATCHDOG() -> dict[str, object]:
    """Return the LATTICE_WATCHDOG component description."""
    return create_component(
        "LATTICE_WATCHDOG",
        "automation",
    )
