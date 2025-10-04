"""Factory for the SYMBOLIC_DNA_ENCODER component."""
from __future__ import annotations

from ..factory import component_factory

SYMBOLIC_DNA_ENCODER = component_factory(__name__, "SYMBOLIC_DNA_ENCODER", "bio")

__all__ = ["SYMBOLIC_DNA_ENCODER"]
