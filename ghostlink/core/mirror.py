"""Factory for the MIRROR component."""
from __future__ import annotations

from ..factory import component_factory

MIRROR = component_factory(__name__, "MIRROR", "core")

__all__ = ["MIRROR"]
