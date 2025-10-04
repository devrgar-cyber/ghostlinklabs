"""HOST component module."""
from __future__ import annotations

from ..blueprint import component_factory


HOST = component_factory("HOST", "core", module=__name__)
