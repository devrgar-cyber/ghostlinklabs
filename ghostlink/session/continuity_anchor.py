"""Factory for the CONTINUITY_ANCHOR component."""
from __future__ import annotations

from ..factory import component_factory

CONTINUITY_ANCHOR = component_factory(__name__, "CONTINUITY_ANCHOR", "session")

__all__ = ["CONTINUITY_ANCHOR"]
