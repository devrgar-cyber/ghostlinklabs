"""GAPS component module."""
from __future__ import annotations

from ..blueprint import component_factory


GAPS = component_factory("GAPS", "core", module=__name__)
