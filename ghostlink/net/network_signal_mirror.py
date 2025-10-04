"""Factory for the NETWORK_SIGNAL_MIRROR component."""
from __future__ import annotations

from ..factory import component_factory

NETWORK_SIGNAL_MIRROR = component_factory(__name__, "NETWORK_SIGNAL_MIRROR", "net")

__all__ = ["NETWORK_SIGNAL_MIRROR"]
