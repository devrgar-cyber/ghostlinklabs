"""SPLICE component module."""
from __future__ import annotations

from ..blueprint import component_factory


SPLICE = component_factory("SPLICE", "core", module=__name__)
