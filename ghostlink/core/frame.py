"""Factory for the FRAME component."""
from __future__ import annotations

from ..factory import component_factory

FRAME = component_factory(__name__, "FRAME", "core")

__all__ = ["FRAME"]
