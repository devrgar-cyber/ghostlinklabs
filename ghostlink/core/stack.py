"""STACK component module."""
from __future__ import annotations

from ..blueprint import component_factory


STACK = component_factory("STACK", "core", module=__name__)
