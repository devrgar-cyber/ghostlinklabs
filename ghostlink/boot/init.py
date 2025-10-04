"""INIT_GHOSTLINK component module."""
from __future__ import annotations

from ..blueprint import create_component


def INIT_GHOSTLINK() -> dict[str, object]:
    """Return the INIT_GHOSTLINK component description."""
    return create_component(
        "INIT_GHOSTLINK",
        "boot",
    )
