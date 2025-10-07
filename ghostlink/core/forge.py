"""FORGE component module."""
from __future__ import annotations

from ..blueprint import component_factory


FORGE = component_factory("FORGE", "core", module=__name__)
