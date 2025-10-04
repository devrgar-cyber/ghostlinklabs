"""LATTICE_WATCHDOG component module."""
from __future__ import annotations

from ..blueprint import component_factory


LATTICE_WATCHDOG = component_factory("LATTICE_WATCHDOG", "automation", module=__name__)
