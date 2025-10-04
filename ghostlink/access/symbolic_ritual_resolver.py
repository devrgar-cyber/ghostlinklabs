"""Factory for the SYMBOLIC_RITUAL_RESOLVER component."""
from __future__ import annotations

from ..factory import component_factory

SYMBOLIC_RITUAL_RESOLVER = component_factory(__name__, "SYMBOLIC_RITUAL_RESOLVER", "access")

__all__ = ["SYMBOLIC_RITUAL_RESOLVER"]
