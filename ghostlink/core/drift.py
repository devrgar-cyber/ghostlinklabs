"""DRIFT component module."""
from __future__ import annotations

from ..blueprint import component_factory


DRIFT = component_factory("DRIFT", "core", module=__name__)
