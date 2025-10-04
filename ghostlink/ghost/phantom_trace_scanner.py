"""Factory for the PHANTOM_TRACE_SCANNER component."""
from __future__ import annotations

from ..factory import component_factory

PHANTOM_TRACE_SCANNER = component_factory(__name__, "PHANTOM_TRACE_SCANNER", "ghost")

__all__ = ["PHANTOM_TRACE_SCANNER"]
