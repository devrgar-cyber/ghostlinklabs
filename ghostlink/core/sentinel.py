"""Factory for the SENTINEL component."""
from __future__ import annotations

from ..factory import component_factory

SENTINEL = component_factory(__name__, "SENTINEL", "core")

__all__ = ["SENTINEL"]
