"""Factory for the PRISM component."""
from __future__ import annotations

from ..factory import component_factory

PRISM = component_factory(__name__, "PRISM", "core")

__all__ = ["PRISM"]
