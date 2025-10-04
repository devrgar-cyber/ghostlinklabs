"""Factory for the OPERATOR_LOOP_FINDER component."""
from __future__ import annotations

from ..factory import component_factory

OPERATOR_LOOP_FINDER = component_factory(__name__, "OPERATOR_LOOP_FINDER", "observer")

__all__ = ["OPERATOR_LOOP_FINDER"]
