"""CONTINUITY_ANCHOR component module."""
from __future__ import annotations

from ..blueprint import create_component


def CONTINUITY_ANCHOR() -> dict[str, object]:
    """Return the CONTINUITY_ANCHOR component description."""
    return create_component(
        "CONTINUITY_ANCHOR",
        "session",
    )
