"""Factory for the FRACTURE_INDEX_MAPPER component."""
from __future__ import annotations

from ..factory import component_factory

FRACTURE_INDEX_MAPPER = component_factory(__name__, "FRACTURE_INDEX_MAPPER", "diagnostic")

__all__ = ["FRACTURE_INDEX_MAPPER"]
