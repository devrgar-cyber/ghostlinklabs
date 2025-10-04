"""SYMBOLIC_FRAGMENT_RECOVERY component module."""
from __future__ import annotations

from ..blueprint import create_component


def SYMBOLIC_FRAGMENT_RECOVERY() -> dict[str, object]:
    """Return the SYMBOLIC_FRAGMENT_RECOVERY component description."""
    return create_component(
        "SYMBOLIC_FRAGMENT_RECOVERY",
        "session",
    )
