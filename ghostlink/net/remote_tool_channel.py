"""Factory for the REMOTE_TOOL_CHANNEL component."""
from __future__ import annotations

from ..factory import component_factory

REMOTE_TOOL_CHANNEL = component_factory(__name__, "REMOTE_TOOL_CHANNEL", "net")

__all__ = ["REMOTE_TOOL_CHANNEL"]
