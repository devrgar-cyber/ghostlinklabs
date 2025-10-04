"""TEST_NODE component module."""
from __future__ import annotations

from ..blueprint import create_component


def TEST_NODE() -> dict[str, object]:
    """Return the TEST_NODE component description."""
    return create_component(
        "TEST_NODE",
        "session",
    )
