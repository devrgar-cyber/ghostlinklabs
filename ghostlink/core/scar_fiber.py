"""SCAR_FIBER component module."""
from __future__ import annotations

from ..blueprint import component_factory


SCAR_FIBER = component_factory("SCAR_FIBER", "core", module=__name__)
