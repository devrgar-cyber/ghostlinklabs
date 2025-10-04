"""TOOL_CHAIN_ORCHESTRATOR component module."""
from __future__ import annotations

from ..blueprint import create_component


def TOOL_CHAIN_ORCHESTRATOR() -> dict[str, object]:
    """Return the TOOL_CHAIN_ORCHESTRATOR component description."""
    return create_component(
        "TOOL_CHAIN_ORCHESTRATOR",
        "automation",
    )
