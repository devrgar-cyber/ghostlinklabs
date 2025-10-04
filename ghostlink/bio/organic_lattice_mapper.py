"""Factory for the ORGANIC_LATTICE_MAPPER component."""
from __future__ import annotations

from ..factory import component_factory

ORGANIC_LATTICE_MAPPER = component_factory(__name__, "ORGANIC_LATTICE_MAPPER", "bio")

__all__ = ["ORGANIC_LATTICE_MAPPER"]
