"""Factory for the IMPLICIT_UNLOCK component."""
from __future__ import annotations

from ..factory import component_factory

IMPLICIT_UNLOCK = component_factory(__name__, "IMPLICIT_UNLOCK", "access")

__all__ = ["IMPLICIT_UNLOCK"]
