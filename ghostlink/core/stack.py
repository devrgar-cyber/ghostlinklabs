"""Factory for the STACK component."""
from __future__ import annotations

from ..factory import component_factory

STACK = component_factory(__name__, "STACK", "core")

__all__ = ["STACK"]
