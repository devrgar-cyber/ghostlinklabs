"""MEMORY component module."""
from __future__ import annotations

from ..blueprint import component_factory


MEMORY = component_factory("MEMORY", "core", module=__name__)
