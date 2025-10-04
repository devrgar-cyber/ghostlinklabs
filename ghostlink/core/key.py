"""KEY component module."""
from __future__ import annotations

from ..blueprint import component_factory


KEY = component_factory("KEY", "core", module=__name__)
