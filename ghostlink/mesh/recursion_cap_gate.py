"""Factory for the RECURSION_CAP_GATE component."""
from __future__ import annotations

from ..factory import component_factory

RECURSION_CAP_GATE = component_factory(__name__, "RECURSION_CAP_GATE", "mesh")

__all__ = ["RECURSION_CAP_GATE"]
