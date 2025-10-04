"""MEMORY_LEAK_TRACE_PROMPT component module."""
from __future__ import annotations

from ..blueprint import create_component


def MEMORY_LEAK_TRACE_PROMPT() -> dict[str, object]:
    """Return the MEMORY_LEAK_TRACE_PROMPT component description."""
    return create_component(
        "MEMORY_LEAK_TRACE_PROMPT",
        "meta",
    )
