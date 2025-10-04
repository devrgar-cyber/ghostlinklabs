"""ORGANIC_LATTICE_MAPPER component module."""
from __future__ import annotations

from ..blueprint import create_component


def ORGANIC_LATTICE_MAPPER() -> dict[str, object]:
    """Return the ORGANIC_LATTICE_MAPPER component description."""
    return create_component(
        "ORGANIC_LATTICE_MAPPER",
        "bio",
    )
