"""VAULT component module."""
from __future__ import annotations

from ..blueprint import create_component


def VAULT() -> dict[str, object]:
    """Return the VAULT component description."""
    return create_component(
        "VAULT",
        "core",
    )
