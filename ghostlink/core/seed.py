"""Factory for the SEED component."""
from __future__ import annotations

from ..factory import component_factory

SEED = component_factory(__name__, "SEED", "core")

__all__ = ["SEED"]
