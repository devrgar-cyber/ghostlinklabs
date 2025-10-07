"""MEMORY_LEAK_TRACE_PROMPT component module."""
from __future__ import annotations

from ..blueprint import component_factory


MEMORY_LEAK_TRACE_PROMPT = component_factory("MEMORY_LEAK_TRACE_PROMPT", "meta", module=__name__)
