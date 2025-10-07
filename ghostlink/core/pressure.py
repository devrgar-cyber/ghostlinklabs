"""PRESSURE component module."""
from __future__ import annotations

from ..blueprint import component_factory


PRESSURE = component_factory("PRESSURE", "core", module=__name__)
