"""Factory for the LIVE_SIGNAL_RENDERER component."""
from __future__ import annotations

from ..factory import component_factory

LIVE_SIGNAL_RENDERER = component_factory(__name__, "LIVE_SIGNAL_RENDERER", "gui")

__all__ = ["LIVE_SIGNAL_RENDERER"]
