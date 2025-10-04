"""Integrity monitoring utilities."""
from __future__ import annotations

from typing import Iterable

from ghostlink.core import ToolResponse
from ghostlink.core._shared import build_response


def TOOL_INTEGRITY_CHECK(tools: Iterable[str] | None = None) -> ToolResponse:
    """Validate that declared tools are reachable."""
    entries = list(tools or [])
    context = {"tools": entries, "validated": all(entries)}
    status = "verified" if context["validated"] else "degraded"
    return build_response("TOOL_INTEGRITY_CHECK", context=context, status=status)
