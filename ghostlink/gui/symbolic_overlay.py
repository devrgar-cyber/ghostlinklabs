"""Factory for the SYMBOLIC_OVERLAY component."""
from __future__ import annotations

from ..factory import component_factory

SYMBOLIC_OVERLAY = component_factory(__name__, "SYMBOLIC_OVERLAY", "gui")

__all__ = ["SYMBOLIC_OVERLAY"]
