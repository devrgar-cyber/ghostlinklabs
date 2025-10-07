"""BIND component module."""
from __future__ import annotations

from ..blueprint import component_factory


BIND = component_factory("BIND", "core", module=__name__)
