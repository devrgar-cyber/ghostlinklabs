"""TUNNEL component module."""
from __future__ import annotations

from ..blueprint import component_factory


TUNNEL = component_factory("TUNNEL", "core", module=__name__)
