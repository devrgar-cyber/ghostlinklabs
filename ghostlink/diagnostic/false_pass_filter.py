"""FALSE_PASS_FILTER component module."""
from __future__ import annotations

from ..blueprint import create_component


def FALSE_PASS_FILTER() -> dict[str, object]:
    """Return the FALSE_PASS_FILTER component description."""
    return create_component(
        "FALSE_PASS_FILTER",
        "diagnostic",
    )
