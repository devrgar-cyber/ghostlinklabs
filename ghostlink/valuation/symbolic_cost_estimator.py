"""Factory for the SYMBOLIC_COST_ESTIMATOR component."""
from __future__ import annotations

from ..factory import component_factory

SYMBOLIC_COST_ESTIMATOR = component_factory(__name__, "SYMBOLIC_COST_ESTIMATOR", "valuation")

__all__ = ["SYMBOLIC_COST_ESTIMATOR"]
