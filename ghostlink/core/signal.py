"""Factory for the SIGNAL component."""
from __future__ import annotations

from ..factory import component_factory

SIGNAL = component_factory(__name__, "SIGNAL", "core")

__all__ = ["SIGNAL"]
