"""SENSORIAL_DIAGNOSTIC_PROMPT component module."""
from __future__ import annotations

from ..blueprint import create_component


def SENSORIAL_DIAGNOSTIC_PROMPT() -> dict[str, object]:
    """Return the SENSORIAL_DIAGNOSTIC_PROMPT component description."""
    return create_component(
        "SENSORIAL_DIAGNOSTIC_PROMPT",
        "meta",
    )
