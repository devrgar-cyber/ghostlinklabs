"""Factory for the RITUAL_UNLOCK component."""
from __future__ import annotations

from ..factory import component_factory

RITUAL_UNLOCK = component_factory(__name__, "RITUAL_UNLOCK", "access")

__all__ = ["RITUAL_UNLOCK"]
