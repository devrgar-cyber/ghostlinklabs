"""SYMBOLIC_COST_ESTIMATOR component module."""
from __future__ import annotations

from ..blueprint import component_factory


SYMBOLIC_COST_ESTIMATOR = component_factory("SYMBOLIC_COST_ESTIMATOR", "valuation", module=__name__)
