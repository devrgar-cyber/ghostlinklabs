"""Factory for the LATTICE_SELF_TEST component."""
from __future__ import annotations

from ..factory import component_factory

LATTICE_SELF_TEST = component_factory(__name__, "LATTICE_SELF_TEST", "test")

__all__ = ["LATTICE_SELF_TEST"]
