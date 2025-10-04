"""GATE component module."""
from __future__ import annotations

from ..blueprint import component_factory


GATE = component_factory("GATE", "core", module=__name__)
