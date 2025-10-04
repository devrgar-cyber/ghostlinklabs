"""ECHO_VIEWPORT component module."""
from __future__ import annotations

from ..blueprint import create_component


def ECHO_VIEWPORT() -> dict[str, object]:
    """Return the ECHO_VIEWPORT component description."""
    return create_component(
        "ECHO_VIEWPORT",
        "gui",
    )
