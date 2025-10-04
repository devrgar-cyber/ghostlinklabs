"""Factory for the SWITCH component."""
from __future__ import annotations

from ..factory import component_factory

SWITCH = component_factory(__name__, "SWITCH", "core")

__all__ = ["SWITCH"]
