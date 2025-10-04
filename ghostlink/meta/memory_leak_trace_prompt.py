"""Factory for the MEMORY_LEAK_TRACE_PROMPT component."""
from __future__ import annotations

from ..factory import component_factory

MEMORY_LEAK_TRACE_PROMPT = component_factory(__name__, "MEMORY_LEAK_TRACE_PROMPT", "meta")

__all__ = ["MEMORY_LEAK_TRACE_PROMPT"]
