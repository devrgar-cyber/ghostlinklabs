"""CURRENT component module."""
from __future__ import annotations

from ..blueprint import component_factory


CURRENT = component_factory("CURRENT", "core", module=__name__)
