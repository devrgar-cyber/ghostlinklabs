"""LOOPED_SELF_OBSERVER component module."""
from __future__ import annotations

from ..blueprint import create_component


def LOOPED_SELF_OBSERVER() -> dict[str, object]:
    """Return the LOOPED_SELF_OBSERVER component description."""
    return create_component(
        "LOOPED_SELF_OBSERVER",
        "reflect",
    )
