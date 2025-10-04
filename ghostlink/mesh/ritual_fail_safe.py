"""RITUAL_FAIL_SAFE component module."""
from __future__ import annotations

from ..blueprint import create_component


def RITUAL_FAIL_SAFE() -> dict[str, object]:
    """Return the RITUAL_FAIL_SAFE component description."""
    return create_component(
        "RITUAL_FAIL_SAFE",
        "mesh",
    )
