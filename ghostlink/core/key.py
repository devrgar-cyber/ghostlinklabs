"""KEY component module."""
from __future__ import annotations

from ..blueprint import create_component


def KEY() -> dict[str, object]:
    """Return the KEY component description."""
    return create_component(
        "KEY",
        "core",
    )
