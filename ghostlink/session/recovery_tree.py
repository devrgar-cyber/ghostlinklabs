"""Factory for the RECOVERY_TREE component."""
from __future__ import annotations

from ..factory import component_factory

RECOVERY_TREE = component_factory(__name__, "RECOVERY_TREE", "session")

__all__ = ["RECOVERY_TREE"]
