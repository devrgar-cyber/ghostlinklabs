"""LINK component module."""
from __future__ import annotations

from ..blueprint import create_component


def LINK() -> dict[str, object]:
    """Return the LINK component description."""
    return create_component(
        "LINK",
        "core",
    )
