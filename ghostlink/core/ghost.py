"""Factory for the GHOST component."""
from __future__ import annotations

from ..factory import component_factory

GHOST = component_factory(__name__, "GHOST", "core")

__all__ = ["GHOST"]
