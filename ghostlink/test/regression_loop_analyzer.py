"""REGRESSION_LOOP_ANALYZER component module."""
from __future__ import annotations

from ..blueprint import component_factory


REGRESSION_LOOP_ANALYZER = component_factory("REGRESSION_LOOP_ANALYZER", "test", module=__name__)
