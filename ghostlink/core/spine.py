"""Factory for the SPINE component."""
from __future__ import annotations

from ..factory import component_factory

SPINE = component_factory(__name__, "SPINE", "core")

__all__ = ["SPINE"]
