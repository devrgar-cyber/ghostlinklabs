"""TEST_SIGNAL_INJECTION component module."""
from __future__ import annotations

from ..blueprint import create_component


def TEST_SIGNAL_INJECTION() -> dict[str, object]:
    """Return the TEST_SIGNAL_INJECTION component description."""
    return create_component(
        "TEST_SIGNAL_INJECTION",
        "sandbox",
    )
