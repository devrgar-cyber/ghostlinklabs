"""SIGNAL component module."""
from __future__ import annotations

from ..blueprint import component_factory


SIGNAL = component_factory("SIGNAL", "core", module=__name__)
