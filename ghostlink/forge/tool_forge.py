"""Factory for the TOOL_FORGE component."""
from __future__ import annotations

from ..factory import component_factory

TOOL_FORGE = component_factory(__name__, "TOOL_FORGE", "forge")

__all__ = ["TOOL_FORGE"]
