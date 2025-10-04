"""Factory for the LATTICE_TRACE component."""
from __future__ import annotations

from ..factory import component_factory

LATTICE_TRACE = component_factory(__name__, "LATTICE_TRACE", "lattice")

__all__ = ["LATTICE_TRACE"]
