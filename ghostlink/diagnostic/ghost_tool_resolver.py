"""GHOST_TOOL_RESOLVER component module."""
from __future__ import annotations

from ..blueprint import component_factory


GHOST_TOOL_RESOLVER = component_factory("GHOST_TOOL_RESOLVER", "diagnostic", module=__name__)
