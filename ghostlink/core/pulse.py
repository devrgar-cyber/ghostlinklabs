"""Factory for the PULSE component."""
from __future__ import annotations

from ..factory import component_factory

PULSE = component_factory(__name__, "PULSE", "core")

__all__ = ["PULSE"]
