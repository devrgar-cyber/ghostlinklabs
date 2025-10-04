"""TRACE component module."""
from __future__ import annotations

from ..blueprint import create_component


def TRACE() -> dict[str, object]:
    """Return the TRACE component description."""
    return create_component(
        "TRACE",
        "core",
    )
