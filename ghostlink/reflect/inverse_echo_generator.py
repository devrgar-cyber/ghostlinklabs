"""INVERSE_ECHO_GENERATOR component module."""
from __future__ import annotations

from ..blueprint import create_component


def INVERSE_ECHO_GENERATOR() -> dict[str, object]:
    """Return the INVERSE_ECHO_GENERATOR component description."""
    return create_component(
        "INVERSE_ECHO_GENERATOR",
        "reflect",
    )
