"""Factory for the SCAR_FIBER component."""
from __future__ import annotations

from ..factory import component_factory

SCAR_FIBER = component_factory(__name__, "SCAR_FIBER", "core")

__all__ = ["SCAR_FIBER"]
