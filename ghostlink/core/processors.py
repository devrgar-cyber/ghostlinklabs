"""PROCESSORS component module."""
from __future__ import annotations

from ..blueprint import create_component


def PROCESSORS() -> dict[str, object]:
    """Return the PROCESSORS component description."""
    return create_component(
        "PROCESSORS",
        "core",
    )
