"""INDEX_SYMBOLIC_TERM component module."""
from __future__ import annotations

from ..blueprint import create_component


def INDEX_SYMBOLIC_TERM() -> dict[str, object]:
    """Return the INDEX_SYMBOLIC_TERM component description."""
    return create_component(
        "INDEX_SYMBOLIC_TERM",
        "lattice",
    )
