"""Factory for the OFFSET component."""
from __future__ import annotations

from ..factory import component_factory

OFFSET = component_factory(__name__, "OFFSET", "core")

__all__ = ["OFFSET"]
