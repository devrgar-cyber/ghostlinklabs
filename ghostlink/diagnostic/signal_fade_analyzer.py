"""Factory for the SIGNAL_FADE_ANALYZER component."""
from __future__ import annotations

from ..factory import component_factory

SIGNAL_FADE_ANALYZER = component_factory(__name__, "SIGNAL_FADE_ANALYZER", "diagnostic")

__all__ = ["SIGNAL_FADE_ANALYZER"]
