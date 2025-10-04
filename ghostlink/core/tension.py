"""Factory for the TENSION component."""
from __future__ import annotations

from ..factory import component_factory

TENSION = component_factory(__name__, "TENSION", "core")

__all__ = ["TENSION"]
