"""Factory for the SCHEMA_MELDER component."""
from __future__ import annotations

from ..factory import component_factory

SCHEMA_MELDER = component_factory(__name__, "SCHEMA_MELDER", "forge")

__all__ = ["SCHEMA_MELDER"]
