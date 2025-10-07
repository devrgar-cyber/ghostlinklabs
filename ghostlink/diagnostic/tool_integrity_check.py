"""TOOL_INTEGRITY_CHECK component module."""
from __future__ import annotations

from ..blueprint import component_factory


TOOL_INTEGRITY_CHECK = component_factory("TOOL_INTEGRITY_CHECK", "diagnostic", module=__name__)
