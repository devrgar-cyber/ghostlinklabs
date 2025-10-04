"""Factory for the DUALITY component."""
from __future__ import annotations

from ..factory import component_factory

DUALITY = component_factory(__name__, "DUALITY", "core")

__all__ = ["DUALITY"]
