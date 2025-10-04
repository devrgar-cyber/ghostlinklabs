"""Factory for the LATTICE_SEED component."""
from __future__ import annotations

from ..factory import component_factory

LATTICE_SEED = component_factory(__name__, "LATTICE_SEED", "lattice")

__all__ = ["LATTICE_SEED"]
