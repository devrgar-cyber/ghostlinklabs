"""REGRESSION_LOOP_ANALYZER component module."""
from __future__ import annotations

from ..blueprint import create_component


def REGRESSION_LOOP_ANALYZER() -> dict[str, object]:
    """Return the REGRESSION_LOOP_ANALYZER component description."""
    return create_component(
        "REGRESSION_LOOP_ANALYZER",
        "test",
    )
