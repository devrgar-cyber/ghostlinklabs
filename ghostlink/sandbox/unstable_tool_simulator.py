"""UNSTABLE_TOOL_SIMULATOR component module."""
from __future__ import annotations

from ..blueprint import create_component


def UNSTABLE_TOOL_SIMULATOR() -> dict[str, object]:
    """Return the UNSTABLE_TOOL_SIMULATOR component description."""
    return create_component(
        "UNSTABLE_TOOL_SIMULATOR",
        "sandbox",
    )
