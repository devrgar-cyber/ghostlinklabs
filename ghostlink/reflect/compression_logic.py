"""Factory for the COMPRESSION_LOGIC component."""
from __future__ import annotations

from ..factory import component_factory

COMPRESSION_LOGIC = component_factory(__name__, "COMPRESSION_LOGIC", "reflect")

__all__ = ["COMPRESSION_LOGIC"]
