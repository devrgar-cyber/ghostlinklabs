"""SYMBOLIC_SPLINTER_PATCH component module."""
from __future__ import annotations

from ..blueprint import component_factory


SYMBOLIC_SPLINTER_PATCH = component_factory("SYMBOLIC_SPLINTER_PATCH", "mesh", module=__name__)
