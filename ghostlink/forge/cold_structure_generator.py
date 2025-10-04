"""Factory for the COLD_STRUCTURE_GENERATOR component."""
from __future__ import annotations

from ..factory import component_factory

COLD_STRUCTURE_GENERATOR = component_factory(__name__, "COLD_STRUCTURE_GENERATOR", "forge")

__all__ = ["COLD_STRUCTURE_GENERATOR"]
