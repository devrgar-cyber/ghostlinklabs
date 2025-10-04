"""LATTICE_SELF_TEST component module."""
from __future__ import annotations

from ..blueprint import create_component


def LATTICE_SELF_TEST() -> dict[str, object]:
    """Return the LATTICE_SELF_TEST component description."""
    return create_component(
        "LATTICE_SELF_TEST",
        "test",
    )
