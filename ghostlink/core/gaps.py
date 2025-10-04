"""Factory for the GAPS component."""
from __future__ import annotations

from ..factory import component_factory

GAPS = component_factory(__name__, "GAPS", "core")

__all__ = ["GAPS"]
