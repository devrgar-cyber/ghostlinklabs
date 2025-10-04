"""ARCHIVE component module."""
from __future__ import annotations

from ..blueprint import create_component


def ARCHIVE() -> dict[str, object]:
    """Return the ARCHIVE component description."""
    return create_component(
        "ARCHIVE",
        "core",
    )
