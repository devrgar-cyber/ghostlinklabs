"""OPERATOR_LOOP_FINDER component module."""
from __future__ import annotations

from ..blueprint import component_factory


OPERATOR_LOOP_FINDER = component_factory("OPERATOR_LOOP_FINDER", "observer", module=__name__)
