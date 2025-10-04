"""HARMONY component module."""
from __future__ import annotations

from ..blueprint import component_factory


HARMONY = component_factory("HARMONY", "core", module=__name__)
