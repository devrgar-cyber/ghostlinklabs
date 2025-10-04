"""Factory for the LENS component."""
from __future__ import annotations

from ..factory import component_factory

LENS = component_factory(__name__, "LENS", "core")

__all__ = ["LENS"]
