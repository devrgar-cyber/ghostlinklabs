"""Factory for the TOOL_INTEGRITY_CHECK component."""
from __future__ import annotations

from ..factory import component_factory

TOOL_INTEGRITY_CHECK = component_factory(__name__, "TOOL_INTEGRITY_CHECK", "diagnostic")

__all__ = ["TOOL_INTEGRITY_CHECK"]
