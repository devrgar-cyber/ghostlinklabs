"""Factory for the DEPTH component."""
from __future__ import annotations

from ..factory import component_factory

DEPTH = component_factory(__name__, "DEPTH", "core")

__all__ = ["DEPTH"]
