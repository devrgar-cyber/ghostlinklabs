"""Factory for the KEY component."""
from __future__ import annotations

from ..factory import component_factory

KEY = component_factory(__name__, "KEY", "core")

__all__ = ["KEY"]
