"""Factory for the FORGE component."""
from __future__ import annotations

from ..factory import component_factory

FORGE = component_factory(__name__, "FORGE", "core")

__all__ = ["FORGE"]
