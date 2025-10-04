"""EDGE_STATE_REGENERATOR component module."""
from __future__ import annotations

from ..blueprint import create_component


def EDGE_STATE_REGENERATOR() -> dict[str, object]:
    """Return the EDGE_STATE_REGENERATOR component description."""
    return create_component(
        "EDGE_STATE_REGENERATOR",
        "mesh",
    )
