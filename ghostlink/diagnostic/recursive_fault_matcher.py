"""RECURSIVE_FAULT_MATCHER component module."""
from __future__ import annotations

from ..blueprint import create_component


def RECURSIVE_FAULT_MATCHER() -> dict[str, object]:
    """Return the RECURSIVE_FAULT_MATCHER component description."""
    return create_component(
        "RECURSIVE_FAULT_MATCHER",
        "diagnostic",
    )
