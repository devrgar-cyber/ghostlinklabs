"""Factory for the CHANNEL_ECHO component."""
from __future__ import annotations

from ..factory import component_factory

CHANNEL_ECHO = component_factory(__name__, "CHANNEL_ECHO", "core")

__all__ = ["CHANNEL_ECHO"]
