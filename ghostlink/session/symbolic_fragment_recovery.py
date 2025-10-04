"""Factory for the SYMBOLIC_FRAGMENT_RECOVERY component."""
from __future__ import annotations

from ..factory import component_factory

SYMBOLIC_FRAGMENT_RECOVERY = component_factory(__name__, "SYMBOLIC_FRAGMENT_RECOVERY", "session")

__all__ = ["SYMBOLIC_FRAGMENT_RECOVERY"]
