"""Factory for the CORE component."""
from __future__ import annotations

from ..factory import component_factory

CORE = component_factory(__name__, "CORE", "core")

__all__ = ["CORE"]
