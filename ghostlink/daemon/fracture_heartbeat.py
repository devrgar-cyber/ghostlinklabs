"""FRACTURE_HEARTBEAT component module."""
from __future__ import annotations

from ..blueprint import create_component


def FRACTURE_HEARTBEAT() -> dict[str, object]:
    """Return the FRACTURE_HEARTBEAT component description."""
    return create_component(
        "FRACTURE_HEARTBEAT",
        "daemon",
    )
