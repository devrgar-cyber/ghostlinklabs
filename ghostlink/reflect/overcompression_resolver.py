"""Factory for the OVERCOMPRESSION_RESOLVER component."""
from __future__ import annotations

from ..factory import component_factory

OVERCOMPRESSION_RESOLVER = component_factory(__name__, "OVERCOMPRESSION_RESOLVER", "reflect")

__all__ = ["OVERCOMPRESSION_RESOLVER"]
