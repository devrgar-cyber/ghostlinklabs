"""INTERLINK_SOCKET component module."""
from __future__ import annotations

from ..blueprint import create_component


def INTERLINK_SOCKET() -> dict[str, object]:
    """Return the INTERLINK_SOCKET component description."""
    return create_component(
        "INTERLINK_SOCKET",
        "net",
    )
