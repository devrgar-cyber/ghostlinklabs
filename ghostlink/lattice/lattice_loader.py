"""Factory for the LATTICE_LOADER component."""
from __future__ import annotations

from ..factory import component_factory

LATTICE_LOADER = component_factory(__name__, "LATTICE_LOADER", "lattice")

__all__ = ["LATTICE_LOADER"]
