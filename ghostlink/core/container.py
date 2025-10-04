"""CONTAINER component module."""
from __future__ import annotations

from ..blueprint import component_factory


CONTAINER = component_factory("CONTAINER", "core", module=__name__)
