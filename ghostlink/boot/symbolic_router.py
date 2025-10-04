"""Factory for the SYMBOLIC_ROUTER component."""
from __future__ import annotations

from ..factory import component_factory

SYMBOLIC_ROUTER = component_factory(__name__, "SYMBOLIC_ROUTER", "boot")

__all__ = ["SYMBOLIC_ROUTER"]
