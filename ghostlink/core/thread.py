"""THREAD component module."""
from __future__ import annotations

from ..blueprint import component_factory


THREAD = component_factory("THREAD", "core", module=__name__)
