"""Factory for the INSPECTION_SEQUENCE component."""
from __future__ import annotations

from ..factory import component_factory

INSPECTION_SEQUENCE = component_factory(__name__, "INSPECTION_SEQUENCE", "session")

__all__ = ["INSPECTION_SEQUENCE"]
