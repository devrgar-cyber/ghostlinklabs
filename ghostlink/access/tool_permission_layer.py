"""Factory for the TOOL_PERMISSION_LAYER component."""
from __future__ import annotations

from ..factory import component_factory

TOOL_PERMISSION_LAYER = component_factory(__name__, "TOOL_PERMISSION_LAYER", "access")

__all__ = ["TOOL_PERMISSION_LAYER"]
