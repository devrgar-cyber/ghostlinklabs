"""Factory for the NEURO_SIGNAL_PROXY component."""
from __future__ import annotations

from ..factory import component_factory

NEURO_SIGNAL_PROXY = component_factory(__name__, "NEURO_SIGNAL_PROXY", "bio")

__all__ = ["NEURO_SIGNAL_PROXY"]
