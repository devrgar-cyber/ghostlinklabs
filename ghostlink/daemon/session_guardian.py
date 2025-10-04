"""SESSION_GUARDIAN component module."""
from __future__ import annotations

from ..blueprint import create_component


def SESSION_GUARDIAN() -> dict[str, object]:
    """Return the SESSION_GUARDIAN component description."""
    return create_component(
        "SESSION_GUARDIAN",
        "daemon",
    )
