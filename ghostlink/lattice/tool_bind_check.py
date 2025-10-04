"""Factory for the TOOL_BIND_CHECK component."""
from __future__ import annotations

from ..factory import component_factory

TOOL_BIND_CHECK = component_factory(__name__, "TOOL_BIND_CHECK", "lattice")

__all__ = ["TOOL_BIND_CHECK"]
