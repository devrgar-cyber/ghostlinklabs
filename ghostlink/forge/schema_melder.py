"""SCHEMA_MELDER component module."""
from __future__ import annotations

from ..blueprint import create_component


def SCHEMA_MELDER() -> dict[str, object]:
    """Return the SCHEMA_MELDER component description."""
    return create_component(
        "SCHEMA_MELDER",
        "forge",
    )
