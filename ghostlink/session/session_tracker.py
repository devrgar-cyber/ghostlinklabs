"""Live diagnostic context tracking."""
from __future__ import annotations

from typing import Dict

from ghostlink.core import ToolResponse
from ghostlink.core._shared import build_response


def SESSION_TRACKER(state: Dict[str, object] | None = None) -> ToolResponse:
    """Track live diagnostic context for a session."""
    context = {"state": state or {}, "active": bool(state)}
    status = "tracking" if context["active"] else "idle"
    return build_response("SESSION_TRACKER", context=context, status=status)
