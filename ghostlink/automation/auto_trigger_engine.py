"""AUTO_TRIGGER_ENGINE component module."""
from __future__ import annotations

from ..blueprint import create_component


def AUTO_TRIGGER_ENGINE() -> dict[str, object]:
    """Return the AUTO_TRIGGER_ENGINE component description."""
    return create_component(
        "AUTO_TRIGGER_ENGINE",
        "automation",
    )
