"""Factory for the TILE component."""
from __future__ import annotations

from ..factory import component_factory

TILE = component_factory(__name__, "TILE", "core")

__all__ = ["TILE"]
