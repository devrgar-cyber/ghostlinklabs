"""SPINE component module."""
from __future__ import annotations

from ..blueprint import component_factory


SPINE = component_factory("SPINE", "core", module=__name__)
