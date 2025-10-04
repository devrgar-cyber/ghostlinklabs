"""Factory for the PRESSURE component."""
from __future__ import annotations

from ..factory import component_factory

PRESSURE = component_factory(__name__, "PRESSURE", "core")

__all__ = ["PRESSURE"]
