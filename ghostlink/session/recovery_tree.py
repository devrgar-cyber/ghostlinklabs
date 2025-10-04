"""RECOVERY_TREE component module."""
from __future__ import annotations

from ..blueprint import create_component


def RECOVERY_TREE() -> dict[str, object]:
    """Return the RECOVERY_TREE component description."""
    return create_component(
        "RECOVERY_TREE",
        "session",
    )
