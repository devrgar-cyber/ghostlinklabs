"""Factory for the LOCK_DELTA component."""
from __future__ import annotations

from ..factory import component_factory

LOCK_DELTA = component_factory(__name__, "LOCK_DELTA", "core")

__all__ = ["LOCK_DELTA"]
