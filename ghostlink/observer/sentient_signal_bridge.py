"""Factory for the SENTIENT_SIGNAL_BRIDGE component."""
from __future__ import annotations

from ..factory import component_factory

SENTIENT_SIGNAL_BRIDGE = component_factory(__name__, "SENTIENT_SIGNAL_BRIDGE", "observer")

__all__ = ["SENTIENT_SIGNAL_BRIDGE"]
