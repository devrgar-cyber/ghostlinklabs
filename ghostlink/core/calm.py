"""CALM component module."""
from __future__ import annotations

from ..blueprint import component_factory


CALM = component_factory("CALM", "core", module=__name__)
