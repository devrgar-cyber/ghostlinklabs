"""OBSERVER_FEEDBACK_UI component module."""
from __future__ import annotations

from ..blueprint import create_component


def OBSERVER_FEEDBACK_UI() -> dict[str, object]:
    """Return the OBSERVER_FEEDBACK_UI component description."""
    return create_component(
        "OBSERVER_FEEDBACK_UI",
        "gui",
    )
