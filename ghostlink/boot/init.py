"""Factory for the INIT component."""
from __future__ import annotations

from ..factory import component_factory

INIT = component_factory(__name__, "INIT", "boot")

__all__ = ["INIT"]
