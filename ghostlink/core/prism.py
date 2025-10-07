"""PRISM component module."""
from __future__ import annotations

from ..blueprint import component_factory


PRISM = component_factory("PRISM", "core", module=__name__)
