"""PATH component module."""
from __future__ import annotations

from ..blueprint import create_component


def PATH() -> dict[str, object]:
    """Return the PATH component description."""
    return create_component(
        "PATH",
        "core",
    )
