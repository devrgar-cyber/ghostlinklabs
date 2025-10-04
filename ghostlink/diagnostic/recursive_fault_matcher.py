"""RECURSIVE_FAULT_MATCHER component module."""
from __future__ import annotations

from ..blueprint import component_factory


RECURSIVE_FAULT_MATCHER = component_factory("RECURSIVE_FAULT_MATCHER", "diagnostic", module=__name__)
