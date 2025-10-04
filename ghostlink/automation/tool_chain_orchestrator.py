"""Factory for the TOOL_CHAIN_ORCHESTRATOR component."""
from __future__ import annotations

from ..factory import component_factory

TOOL_CHAIN_ORCHESTRATOR = component_factory(__name__, "TOOL_CHAIN_ORCHESTRATOR", "automation")

__all__ = ["TOOL_CHAIN_ORCHESTRATOR"]
