"""SESSION_TRACKER component module."""
from __future__ import annotations

from ..blueprint import create_component


def SESSION_TRACKER() -> dict[str, object]:
    """Return the SESSION_TRACKER component description."""
    return create_component(
        "SESSION_TRACKER",
        "session",
    )
