"""Factory for the UNSTABLE_TOOL_SIMULATOR component."""
from __future__ import annotations

from ..factory import component_factory

UNSTABLE_TOOL_SIMULATOR = component_factory(__name__, "UNSTABLE_TOOL_SIMULATOR", "sandbox")

__all__ = ["UNSTABLE_TOOL_SIMULATOR"]
