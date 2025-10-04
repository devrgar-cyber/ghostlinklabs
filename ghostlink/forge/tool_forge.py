"""TOOL_FORGE component module."""
from __future__ import annotations

from ..blueprint import component_factory


TOOL_FORGE = component_factory("TOOL_FORGE", "forge", module=__name__)
