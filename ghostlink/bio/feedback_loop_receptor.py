"""FEEDBACK_LOOP_RECEPTOR component module."""
from __future__ import annotations

from ..blueprint import create_component


def FEEDBACK_LOOP_RECEPTOR() -> dict[str, object]:
    """Return the FEEDBACK_LOOP_RECEPTOR component description."""
    return create_component(
        "FEEDBACK_LOOP_RECEPTOR",
        "bio",
    )
