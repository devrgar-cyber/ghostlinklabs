"""LOAD_VAULT component module."""
from __future__ import annotations

from ..blueprint import create_component


def LOAD_VAULT() -> dict[str, object]:
    """Return the LOAD_VAULT component description."""
    return create_component(
        "LOAD_VAULT",
        "boot",
    )
