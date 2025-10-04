"""UNSTABLE_TERM_LINK_SCANNER component module."""
from __future__ import annotations

from ..blueprint import create_component


def UNSTABLE_TERM_LINK_SCANNER() -> dict[str, object]:
    """Return the UNSTABLE_TERM_LINK_SCANNER component description."""
    return create_component(
        "UNSTABLE_TERM_LINK_SCANNER",
        "lattice",
    )
