"""Factory for the SYMBOLIC_PROTOCOL_ROUTER component."""
from __future__ import annotations

from ..factory import component_factory

SYMBOLIC_PROTOCOL_ROUTER = component_factory(__name__, "SYMBOLIC_PROTOCOL_ROUTER", "net")

__all__ = ["SYMBOLIC_PROTOCOL_ROUTER"]
