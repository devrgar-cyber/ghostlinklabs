"""BIND component module."""
from __future__ import annotations

from ..blueprint import create_component


def BIND() -> dict[str, object]:
    """Return the BIND component description."""
    return create_component(
        "BIND",
        "core",
    )
