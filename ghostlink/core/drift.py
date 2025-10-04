"""Factory for the DRIFT component."""
from __future__ import annotations

from ..factory import component_factory

DRIFT = component_factory(__name__, "DRIFT", "core")

__all__ = ["DRIFT"]
