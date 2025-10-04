"""AUTONOMOUS_REPAIR_LOOP component module."""
from __future__ import annotations

from ..blueprint import create_component


def AUTONOMOUS_REPAIR_LOOP() -> dict[str, object]:
    """Return the AUTONOMOUS_REPAIR_LOOP component description."""
    return create_component(
        "AUTONOMOUS_REPAIR_LOOP",
        "automation",
    )
