"""Factory for the SYMBOLIC_CLOCK component."""
from __future__ import annotations

from ..factory import component_factory

SYMBOLIC_CLOCK = component_factory(__name__, "SYMBOLIC_CLOCK", "runtime")

__all__ = ["SYMBOLIC_CLOCK"]
