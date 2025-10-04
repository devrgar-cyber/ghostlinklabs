"""Recursive pressure fabric and agent linking utilities."""
from __future__ import annotations

from typing import Iterable

from ghostlink.core import ToolResponse
from ghostlink.core._shared import build_response


def RECURSION_MESH(nodes: Iterable[str] | None = None) -> ToolResponse:
    """Describe the recursion mesh that links symbolic agents."""
    entries = list(nodes or [])
    context = {"nodes": entries, "depth": len(entries)}
    return build_response("RECURSION_MESH", context=context, status="knit")
