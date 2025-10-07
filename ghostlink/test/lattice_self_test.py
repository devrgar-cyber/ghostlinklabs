"""LATTICE_SELF_TEST component module."""
from __future__ import annotations

from ..blueprint import component_factory


LATTICE_SELF_TEST = component_factory("LATTICE_SELF_TEST", "test", module=__name__)
