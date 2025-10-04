"""SWITCH component module."""
from __future__ import annotations

from ..blueprint import component_factory


SWITCH = component_factory("SWITCH", "core", module=__name__)
