"""MEMORY_REGISTER component module."""
from __future__ import annotations

from ..blueprint import component_factory


MEMORY_REGISTER = component_factory("MEMORY_REGISTER", "runtime", module=__name__)
