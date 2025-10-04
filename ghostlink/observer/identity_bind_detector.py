"""IDENTITY_BIND_DETECTOR component module."""
from __future__ import annotations

from ..blueprint import create_component


def IDENTITY_BIND_DETECTOR() -> dict[str, object]:
    """Return the IDENTITY_BIND_DETECTOR component description."""
    return create_component(
        "IDENTITY_BIND_DETECTOR",
        "observer",
    )
