"""GRID component module."""
from __future__ import annotations

from ..blueprint import component_factory


GRID = component_factory("GRID", "core", module=__name__)
