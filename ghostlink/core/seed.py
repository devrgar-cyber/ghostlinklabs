"""SEED component module."""
from __future__ import annotations

from ..blueprint import component_factory


SEED = component_factory("SEED", "core", module=__name__)
