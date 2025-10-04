"""CONTAINER component module."""
from __future__ import annotations

from ..blueprint import create_component


def CONTAINER() -> dict[str, object]:
    """Return the CONTAINER component description."""
    return create_component(
        "CONTAINER",
        "core",
    )
