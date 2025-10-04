"""Factory for the SPLICE component."""
from __future__ import annotations

from ..factory import component_factory

SPLICE = component_factory(__name__, "SPLICE", "core")

__all__ = ["SPLICE"]
