"""Factory for the REGRESSION_LOOP_ANALYZER component."""
from __future__ import annotations

from ..factory import component_factory

REGRESSION_LOOP_ANALYZER = component_factory(__name__, "REGRESSION_LOOP_ANALYZER", "test")

__all__ = ["REGRESSION_LOOP_ANALYZER"]
