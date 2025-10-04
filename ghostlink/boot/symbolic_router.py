"""ROUTE_SIGNAL component module."""
from __future__ import annotations

from ..blueprint import create_component


def ROUTE_SIGNAL() -> dict[str, object]:
    """Return the ROUTE_SIGNAL component description."""
    return create_component(
        "ROUTE_SIGNAL",
        "boot",
    )
