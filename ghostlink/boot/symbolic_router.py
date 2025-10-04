"""ROUTE_SIGNAL component module."""
from __future__ import annotations

from ..blueprint import component_factory


ROUTE_SIGNAL = component_factory("ROUTE_SIGNAL", "boot", module=__name__)
