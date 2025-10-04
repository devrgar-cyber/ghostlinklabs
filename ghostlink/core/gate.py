"""Factory for the GATE component."""
from __future__ import annotations

from ..factory import component_factory

GATE = component_factory(__name__, "GATE", "core")

__all__ = ["GATE"]
