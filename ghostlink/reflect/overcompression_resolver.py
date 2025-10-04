"""OVERCOMPRESSION_RESOLVER component module."""
from __future__ import annotations

from ..blueprint import component_factory


OVERCOMPRESSION_RESOLVER = component_factory("OVERCOMPRESSION_RESOLVER", "reflect", module=__name__)
