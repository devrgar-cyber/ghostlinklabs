"""Factory for the ARCHIVE component."""
from __future__ import annotations

from ..factory import component_factory

ARCHIVE = component_factory(__name__, "ARCHIVE", "core")

__all__ = ["ARCHIVE"]
