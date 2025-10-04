"""SESSION_EXECUTOR component module."""
from __future__ import annotations

from ..blueprint import create_component


def SESSION_EXECUTOR() -> dict[str, object]:
    """Return the SESSION_EXECUTOR component description."""
    return create_component(
        "SESSION_EXECUTOR",
        "runtime",
    )
