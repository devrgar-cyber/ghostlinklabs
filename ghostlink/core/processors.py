"""Factory for the PROCESSORS component."""
from __future__ import annotations

from ..factory import component_factory

PROCESSORS = component_factory(__name__, "PROCESSORS", "core")

__all__ = ["PROCESSORS"]
