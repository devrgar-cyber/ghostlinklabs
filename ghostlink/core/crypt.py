"""CRYPT component module."""
from __future__ import annotations

from ..blueprint import create_component


def CRYPT() -> dict[str, object]:
    """Return the CRYPT component description."""
    return create_component(
        "CRYPT",
        "core",
    )
