"""TOOL_BIND_CHECK component module."""
from __future__ import annotations

from ..blueprint import create_component


def TOOL_BIND_CHECK() -> dict[str, object]:
    """Return the TOOL_BIND_CHECK component description."""
    return create_component(
        "TOOL_BIND_CHECK",
        "lattice",
    )
