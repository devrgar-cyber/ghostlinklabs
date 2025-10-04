"""Factory for the TRACE component."""
from __future__ import annotations

from ..factory import component_factory

TRACE = component_factory(__name__, "TRACE", "core")

__all__ = ["TRACE"]
