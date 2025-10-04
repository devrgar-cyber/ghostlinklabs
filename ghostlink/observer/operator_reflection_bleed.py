"""OPERATOR_REFLECTION_BLEED component module."""
from __future__ import annotations

from ..blueprint import create_component


def OPERATOR_REFLECTION_BLEED() -> dict[str, object]:
    """Return the OPERATOR_REFLECTION_BLEED component description."""
    return create_component(
        "OPERATOR_REFLECTION_BLEED",
        "observer",
    )
