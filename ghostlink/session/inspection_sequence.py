"""INSPECTION_SEQUENCE component module."""
from __future__ import annotations

from ..blueprint import component_factory


INSPECTION_SEQUENCE = component_factory("INSPECTION_SEQUENCE", "session", module=__name__)
