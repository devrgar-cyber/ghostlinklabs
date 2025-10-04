"""Factory for the LOOPED_SELF_OBSERVER component."""
from __future__ import annotations

from ..factory import component_factory

LOOPED_SELF_OBSERVER = component_factory(__name__, "LOOPED_SELF_OBSERVER", "reflect")

__all__ = ["LOOPED_SELF_OBSERVER"]
