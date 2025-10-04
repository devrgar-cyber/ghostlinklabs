"""Factory for the STATIC component."""
from __future__ import annotations

from ..factory import component_factory

STATIC = component_factory(__name__, "STATIC", "core")

__all__ = ["STATIC"]
