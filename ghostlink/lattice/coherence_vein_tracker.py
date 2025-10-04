"""COHERENCE_VEIN_TRACKER component module."""
from __future__ import annotations

from ..blueprint import create_component


def COHERENCE_VEIN_TRACKER() -> dict[str, object]:
    """Return the COHERENCE_VEIN_TRACKER component description."""
    return create_component(
        "COHERENCE_VEIN_TRACKER",
        "lattice",
    )
