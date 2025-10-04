"""LENS component module."""
from __future__ import annotations

from ..blueprint import component_factory


LENS = component_factory("LENS", "core", module=__name__)
