"""PHANTOM_TRACE_SCANNER component module."""
from __future__ import annotations

from ..blueprint import component_factory


PHANTOM_TRACE_SCANNER = component_factory("PHANTOM_TRACE_SCANNER", "ghost", module=__name__)
