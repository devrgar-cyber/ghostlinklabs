"""Factory for the GHOST_TENSION_MAP component."""
from __future__ import annotations

from ..factory import component_factory

GHOST_TENSION_MAP = component_factory(__name__, "GHOST_TENSION_MAP", "mesh")

__all__ = ["GHOST_TENSION_MAP"]
