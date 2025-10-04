"""Factory for the SYMBOLIC_DECAY_SIMULATOR component."""
from __future__ import annotations

from ..factory import component_factory

SYMBOLIC_DECAY_SIMULATOR = component_factory(__name__, "SYMBOLIC_DECAY_SIMULATOR", "ghost")

__all__ = ["SYMBOLIC_DECAY_SIMULATOR"]
