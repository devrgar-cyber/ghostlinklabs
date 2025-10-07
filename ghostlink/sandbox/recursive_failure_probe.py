"""RECURSIVE_FAILURE_PROBE component module."""
from __future__ import annotations

from ..blueprint import component_factory


RECURSIVE_FAILURE_PROBE = component_factory("RECURSIVE_FAILURE_PROBE", "sandbox", module=__name__)
