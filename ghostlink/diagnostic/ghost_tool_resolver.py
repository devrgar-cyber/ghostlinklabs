"""Resolve tool invocations produced by echoes or residues."""
from __future__ import annotations

from typing import Dict

from ghostlink.core import ToolResponse
from ghostlink.core._shared import build_response


def GHOST_TOOL_RESOLVER(request: Dict[str, str] | None = None) -> ToolResponse:
    """Resolve ghost tool references into canonical tool names."""
    mapping = request or {}
    context = {"request": mapping, "resolved": {k: v.upper() for k, v in mapping.items()}}
    return build_response("GHOST_TOOL_RESOLVER", context=context, status="resolved")
