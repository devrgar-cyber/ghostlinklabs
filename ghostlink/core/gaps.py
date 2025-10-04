"""GAPS component module."""
from __future__ import annotations

from ..blueprint import create_component


def GAPS() -> dict[str, object]:
    """Return the GAPS component description."""
    return create_component(
        "GAPS",
        "core",
    )
