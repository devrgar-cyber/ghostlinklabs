"""GLASS component module."""
from __future__ import annotations

from ..blueprint import component_factory


GLASS = component_factory("GLASS", "core", module=__name__)
