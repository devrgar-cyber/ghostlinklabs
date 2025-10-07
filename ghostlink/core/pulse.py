"""PULSE component module."""
from __future__ import annotations

from ..blueprint import component_factory


PULSE = component_factory("PULSE", "core", module=__name__)
