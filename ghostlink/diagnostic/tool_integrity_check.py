"""TOOL_INTEGRITY_CHECK component module."""
from __future__ import annotations

from ..blueprint import create_component


def TOOL_INTEGRITY_CHECK() -> dict[str, object]:
    """Return the TOOL_INTEGRITY_CHECK component description."""
    return create_component(
        "TOOL_INTEGRITY_CHECK",
        "diagnostic",
    )
