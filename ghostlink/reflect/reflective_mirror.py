"""Factory for the REFLECTIVE_MIRROR component."""
from __future__ import annotations

from ..factory import component_factory

REFLECTIVE_MIRROR = component_factory(__name__, "REFLECTIVE_MIRROR", "reflect")

__all__ = ["REFLECTIVE_MIRROR"]
