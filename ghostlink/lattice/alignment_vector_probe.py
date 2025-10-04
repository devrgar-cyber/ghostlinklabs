"""Factory for the ALIGNMENT_VECTOR_PROBE component."""
from __future__ import annotations

from ..factory import component_factory

ALIGNMENT_VECTOR_PROBE = component_factory(__name__, "ALIGNMENT_VECTOR_PROBE", "lattice")

__all__ = ["ALIGNMENT_VECTOR_PROBE"]
