"""Factory for the THREAD component."""
from __future__ import annotations

from ..factory import component_factory

THREAD = component_factory(__name__, "THREAD", "core")

__all__ = ["THREAD"]
