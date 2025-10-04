"""TOOL_PERMISSION_LAYER component module."""
from __future__ import annotations

from ..blueprint import component_factory


TOOL_PERMISSION_LAYER = component_factory("TOOL_PERMISSION_LAYER", "access", module=__name__)
