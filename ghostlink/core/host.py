"""HOST component module."""
from __future__ import annotations

from ..blueprint import create_component


def HOST() -> dict[str, object]:
    """Return the HOST component description."""
    return create_component(
        "HOST",
        "core",
    )
