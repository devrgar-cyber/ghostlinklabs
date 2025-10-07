"""FRAME component module."""
from __future__ import annotations

from ..blueprint import component_factory


FRAME = component_factory("FRAME", "core", module=__name__)
