"""Factory for the GLASS component."""
from __future__ import annotations

from ..factory import component_factory

GLASS = component_factory(__name__, "GLASS", "core")

__all__ = ["GLASS"]
