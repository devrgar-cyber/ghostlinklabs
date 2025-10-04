"""Factory for the SURFACE component."""
from __future__ import annotations

from ..factory import component_factory

SURFACE = component_factory(__name__, "SURFACE", "core")

__all__ = ["SURFACE"]
