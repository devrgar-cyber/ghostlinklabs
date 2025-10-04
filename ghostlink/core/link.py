"""LINK component module."""
from __future__ import annotations

from ..blueprint import component_factory


LINK = component_factory("LINK", "core", module=__name__)
