"""SURFACE component module."""
from __future__ import annotations

from ..blueprint import component_factory


SURFACE = component_factory("SURFACE", "core", module=__name__)
