"""SYMBOLIC_COST_ESTIMATOR component module."""
from __future__ import annotations

from ..blueprint import create_component


def SYMBOLIC_COST_ESTIMATOR() -> dict[str, object]:
    """Return the SYMBOLIC_COST_ESTIMATOR component description."""
    return create_component(
        "SYMBOLIC_COST_ESTIMATOR",
        "valuation",
    )
