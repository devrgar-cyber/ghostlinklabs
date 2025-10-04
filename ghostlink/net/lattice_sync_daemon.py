"""LATTICE_SYNC_DAEMON component module."""
from __future__ import annotations

from ..blueprint import create_component


def LATTICE_SYNC_DAEMON() -> dict[str, object]:
    """Return the LATTICE_SYNC_DAEMON component description."""
    return create_component(
        "LATTICE_SYNC_DAEMON",
        "net",
    )
