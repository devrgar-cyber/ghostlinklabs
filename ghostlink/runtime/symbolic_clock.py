"""SYMBOLIC_CLOCK component module."""
from __future__ import annotations

from ..blueprint import component_factory


SYMBOLIC_CLOCK = component_factory("SYMBOLIC_CLOCK", "runtime", module=__name__)
