"""MARKER component module."""
from __future__ import annotations

from ..blueprint import component_factory


MARKER = component_factory("MARKER", "core", module=__name__)
