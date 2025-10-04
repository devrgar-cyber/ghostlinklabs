"""Factory for the SYMBOLIC_ALLOY component."""
from __future__ import annotations

from ..factory import component_factory

SYMBOLIC_ALLOY = component_factory(__name__, "SYMBOLIC_ALLOY", "forge")

__all__ = ["SYMBOLIC_ALLOY"]
