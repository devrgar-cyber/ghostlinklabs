"""TRACE component module."""
from __future__ import annotations

from ..blueprint import component_factory


TRACE = component_factory("TRACE", "core", module=__name__)
