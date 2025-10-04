"""Factory for the THRESHOLD component."""
from __future__ import annotations

from ..factory import component_factory

THRESHOLD = component_factory(__name__, "THRESHOLD", "core")

__all__ = ["THRESHOLD"]
