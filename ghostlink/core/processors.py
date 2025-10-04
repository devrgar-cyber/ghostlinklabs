"""PROCESSORS component module."""
from __future__ import annotations

from ..blueprint import component_factory


PROCESSORS = component_factory("PROCESSORS", "core", module=__name__)
