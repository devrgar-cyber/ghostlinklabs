"""ACCESS_PSYCHIC_PROMPT component module."""
from __future__ import annotations

from ..blueprint import create_component


def ACCESS_PSYCHIC_PROMPT() -> dict[str, object]:
    """Return the ACCESS_PSYCHIC_PROMPT component description."""
    return create_component(
        "ACCESS_PSYCHIC_PROMPT",
        "meta",
    )
