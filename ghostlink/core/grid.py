"""Factory for the GRID component."""
from __future__ import annotations

from ..factory import component_factory

GRID = component_factory(__name__, "GRID", "core")

__all__ = ["GRID"]
