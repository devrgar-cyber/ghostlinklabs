"""HARMONY component module."""
from __future__ import annotations

from ..blueprint import create_component


def HARMONY() -> dict[str, object]:
    """Return the HARMONY component description."""
    return create_component(
        "HARMONY",
        "core",
    )
