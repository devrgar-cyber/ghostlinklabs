"""OPERATOR_LOOP_FINDER component module."""
from __future__ import annotations

from ..blueprint import create_component


def OPERATOR_LOOP_FINDER() -> dict[str, object]:
    """Return the OPERATOR_LOOP_FINDER component description."""
    return create_component(
        "OPERATOR_LOOP_FINDER",
        "observer",
    )
