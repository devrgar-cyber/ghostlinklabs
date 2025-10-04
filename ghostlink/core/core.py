"""CORE component module."""
from __future__ import annotations

from ..blueprint import component_factory


CORE = component_factory("CORE", "core", module=__name__)
