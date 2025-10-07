"""TOOL_CHAIN_ORCHESTRATOR component module."""
from __future__ import annotations

from ..blueprint import component_factory


TOOL_CHAIN_ORCHESTRATOR = component_factory("TOOL_CHAIN_ORCHESTRATOR", "automation", module=__name__)
