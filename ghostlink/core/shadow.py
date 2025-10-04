"""Factory for the SHADOW component."""
from __future__ import annotations

from ..factory import component_factory

SHADOW = component_factory(__name__, "SHADOW", "core")

__all__ = ["SHADOW"]
