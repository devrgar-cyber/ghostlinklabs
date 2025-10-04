"""Factory for the MEMORY component."""
from __future__ import annotations

from ..factory import component_factory

MEMORY = component_factory(__name__, "MEMORY", "core")

__all__ = ["MEMORY"]
