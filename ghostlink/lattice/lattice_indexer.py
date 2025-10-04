"""Factory for the LATTICE_INDEXER component."""
from __future__ import annotations

from ..factory import component_factory

LATTICE_INDEXER = component_factory(__name__, "LATTICE_INDEXER", "lattice")

__all__ = ["LATTICE_INDEXER"]
