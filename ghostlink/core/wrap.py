"""Factory for the WRAP component."""
from __future__ import annotations

from ..factory import component_factory

WRAP = component_factory(__name__, "WRAP", "core")

__all__ = ["WRAP"]
