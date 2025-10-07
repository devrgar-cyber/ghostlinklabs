"""SENTINEL component module."""
from __future__ import annotations

from ..blueprint import component_factory


SENTINEL = component_factory("SENTINEL", "core", module=__name__)
