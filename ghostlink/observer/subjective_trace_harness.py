"""SUBJECTIVE_TRACE_HARNESS component module."""
from __future__ import annotations

from ..blueprint import component_factory


SUBJECTIVE_TRACE_HARNESS = component_factory("SUBJECTIVE_TRACE_HARNESS", "observer", module=__name__)
