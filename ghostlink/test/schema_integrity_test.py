"""SCHEMA_INTEGRITY_TEST component module."""
from __future__ import annotations

from ..blueprint import create_component


def SCHEMA_INTEGRITY_TEST() -> dict[str, object]:
    """Return the SCHEMA_INTEGRITY_TEST component description."""
    return create_component(
        "SCHEMA_INTEGRITY_TEST",
        "test",
    )
