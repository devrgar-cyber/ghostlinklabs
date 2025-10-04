"""RITUAL_INTERACTION_MAP component module."""
from __future__ import annotations

from ..blueprint import create_component


def RITUAL_INTERACTION_MAP() -> dict[str, object]:
    """Return the RITUAL_INTERACTION_MAP component description."""
    return create_component(
        "RITUAL_INTERACTION_MAP",
        "gui",
    )
