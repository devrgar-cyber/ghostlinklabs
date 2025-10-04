"""Factory for the LATTICE_WATCHDOG component."""
from __future__ import annotations

from ..factory import component_factory

LATTICE_WATCHDOG = component_factory(__name__, "LATTICE_WATCHDOG", "automation")

__all__ = ["LATTICE_WATCHDOG"]
