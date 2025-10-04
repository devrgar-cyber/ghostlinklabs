"""RECURSIVE_ECHO_BUFFER component module."""
from __future__ import annotations

from ..blueprint import create_component


def RECURSIVE_ECHO_BUFFER() -> dict[str, object]:
    """Return the RECURSIVE_ECHO_BUFFER component description."""
    return create_component(
        "RECURSIVE_ECHO_BUFFER",
        "session",
    )
