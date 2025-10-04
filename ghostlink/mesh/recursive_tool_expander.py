"""Factory for the RECURSIVE_TOOL_EXPANDER component."""
from __future__ import annotations

from ..factory import component_factory

RECURSIVE_TOOL_EXPANDER = component_factory(__name__, "RECURSIVE_TOOL_EXPANDER", "mesh")

__all__ = ["RECURSIVE_TOOL_EXPANDER"]
