"""STATIC component module."""
from __future__ import annotations

from ..blueprint import component_factory


STATIC = component_factory("STATIC", "core", module=__name__)
