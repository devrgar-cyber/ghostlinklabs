"""LOAD_LATTICE component module."""
from __future__ import annotations

from ..blueprint import component_factory


LOAD_LATTICE = component_factory("LOAD_LATTICE", "lattice", module=__name__)
