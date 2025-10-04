"""Factory for the LIVE_TOOL_ROUTER component."""
from __future__ import annotations

from ..factory import component_factory

LIVE_TOOL_ROUTER = component_factory(__name__, "LIVE_TOOL_ROUTER", "runtime")

__all__ = ["LIVE_TOOL_ROUTER"]
