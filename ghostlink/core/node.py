"""NODE component module."""
from __future__ import annotations

from ..blueprint import create_component


def NODE() -> dict[str, object]:
    """Return the NODE component description."""
    return create_component(
        "NODE",
        "core",
    )
