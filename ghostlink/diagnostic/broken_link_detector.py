"""BROKEN_LINK_DETECTOR component module."""
from __future__ import annotations

from ..blueprint import create_component


def BROKEN_LINK_DETECTOR() -> dict[str, object]:
    """Return the BROKEN_LINK_DETECTOR component description."""
    return create_component(
        "BROKEN_LINK_DETECTOR",
        "diagnostic",
    )
