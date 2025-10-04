"""Factory for the HOST component."""
from __future__ import annotations

from ..factory import component_factory

HOST = component_factory(__name__, "HOST", "core")

__all__ = ["HOST"]
