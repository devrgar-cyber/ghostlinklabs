"""PRISM component module."""
from __future__ import annotations

from ..blueprint import create_component


def PRISM() -> dict[str, object]:
    """Return the PRISM component description."""
    return create_component(
        "PRISM",
        "core",
    )
