"""Factory for the BIND component."""
from __future__ import annotations

from ..factory import component_factory

BIND = component_factory(__name__, "BIND", "core")

__all__ = ["BIND"]
