"""Factory for the GHOST_TOOL_RESOLVER component."""
from __future__ import annotations

from ..factory import component_factory

GHOST_TOOL_RESOLVER = component_factory(__name__, "GHOST_TOOL_RESOLVER", "diagnostic")

__all__ = ["GHOST_TOOL_RESOLVER"]
