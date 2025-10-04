"""Factory for the LINK component."""
from __future__ import annotations

from ..factory import component_factory

LINK = component_factory(__name__, "LINK", "core")

__all__ = ["LINK"]
