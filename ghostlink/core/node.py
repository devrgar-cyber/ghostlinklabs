"""Factory for the NODE component."""
from __future__ import annotations

from ..factory import component_factory

NODE = component_factory(__name__, "NODE", "core")

__all__ = ["NODE"]
