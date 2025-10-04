"""Factory for the RESONANCE component."""
from __future__ import annotations

from ..factory import component_factory

RESONANCE = component_factory(__name__, "RESONANCE", "core")

__all__ = ["RESONANCE"]
