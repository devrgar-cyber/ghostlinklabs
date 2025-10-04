"""Factory for the MARKER component."""
from __future__ import annotations

from ..factory import component_factory

MARKER = component_factory(__name__, "MARKER", "core")

__all__ = ["MARKER"]
