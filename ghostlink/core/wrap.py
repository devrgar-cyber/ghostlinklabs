"""WRAP component module."""
from __future__ import annotations

from ..blueprint import component_factory


WRAP = component_factory("WRAP", "core", module=__name__)
