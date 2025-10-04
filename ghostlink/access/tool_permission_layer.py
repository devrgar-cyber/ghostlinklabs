"""TOOL_PERMISSION_LAYER component module."""
from __future__ import annotations

from ..blueprint import create_component


def TOOL_PERMISSION_LAYER() -> dict[str, object]:
    """Return the TOOL_PERMISSION_LAYER component description."""
    return create_component(
        "TOOL_PERMISSION_LAYER",
        "access",
    )
