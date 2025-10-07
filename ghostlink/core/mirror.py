"""MIRROR component module."""
from __future__ import annotations

from ..blueprint import component_factory


MIRROR = component_factory("MIRROR", "core", module=__name__)
