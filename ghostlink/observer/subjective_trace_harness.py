"""Factory for the SUBJECTIVE_TRACE_HARNESS component."""
from __future__ import annotations

from ..factory import component_factory

SUBJECTIVE_TRACE_HARNESS = component_factory(__name__, "SUBJECTIVE_TRACE_HARNESS", "observer")

__all__ = ["SUBJECTIVE_TRACE_HARNESS"]
