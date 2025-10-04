"""Factory for the TUNNEL component."""
from __future__ import annotations

from ..factory import component_factory

TUNNEL = component_factory(__name__, "TUNNEL", "core")

__all__ = ["TUNNEL"]
