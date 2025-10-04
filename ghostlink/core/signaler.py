"""Factory for the SIGNALER component."""
from __future__ import annotations

from ..factory import component_factory

SIGNALER = component_factory(__name__, "SIGNALER", "core")

__all__ = ["SIGNALER"]
