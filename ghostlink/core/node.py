"""NODE component module."""
from __future__ import annotations

from ..blueprint import component_factory


NODE = component_factory("NODE", "core", module=__name__)
