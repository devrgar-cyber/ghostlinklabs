"""Factory for the BROKEN_LINK_DETECTOR component."""
from __future__ import annotations

from ..factory import component_factory

BROKEN_LINK_DETECTOR = component_factory(__name__, "BROKEN_LINK_DETECTOR", "diagnostic")

__all__ = ["BROKEN_LINK_DETECTOR"]
