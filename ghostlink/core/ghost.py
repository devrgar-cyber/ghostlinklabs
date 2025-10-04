"""GHOST component module."""
from __future__ import annotations

from ..blueprint import component_factory


GHOST = component_factory("GHOST", "core", module=__name__)
