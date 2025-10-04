"""Factory for the SYMBOLIC_FIELD_SEED component."""
from __future__ import annotations

from ..factory import component_factory

SYMBOLIC_FIELD_SEED = component_factory(__name__, "SYMBOLIC_FIELD_SEED", "mesh")

__all__ = ["SYMBOLIC_FIELD_SEED"]
