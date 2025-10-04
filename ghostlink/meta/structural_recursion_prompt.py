"""STRUCTURAL_RECURSION_PROMPT component module."""
from __future__ import annotations

from ..blueprint import create_component


def STRUCTURAL_RECURSION_PROMPT() -> dict[str, object]:
    """Return the STRUCTURAL_RECURSION_PROMPT component description."""
    return create_component(
        "STRUCTURAL_RECURSION_PROMPT",
        "meta",
    )
