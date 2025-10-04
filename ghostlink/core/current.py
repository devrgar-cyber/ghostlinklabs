"""Factory for the CURRENT component."""
from __future__ import annotations

from ..factory import component_factory

CURRENT = component_factory(__name__, "CURRENT", "core")

__all__ = ["CURRENT"]
