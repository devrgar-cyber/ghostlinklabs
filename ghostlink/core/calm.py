"""Factory for the CALM component."""
from __future__ import annotations

from ..factory import component_factory

CALM = component_factory(__name__, "CALM", "core")

__all__ = ["CALM"]
