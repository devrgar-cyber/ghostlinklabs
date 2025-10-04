"""ACCESS_RIGHTS_PROMPT component module."""
from __future__ import annotations

from ..blueprint import create_component


def ACCESS_RIGHTS_PROMPT() -> dict[str, object]:
    """Return the ACCESS_RIGHTS_PROMPT component description."""
    return create_component(
        "ACCESS_RIGHTS_PROMPT",
        "meta",
    )
