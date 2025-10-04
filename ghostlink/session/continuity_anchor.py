"""Session continuity anchoring."""
from __future__ import annotations

from typing import Dict

from ghostlink.core import ToolResponse
from ghostlink.core._shared import build_response


def CONTINUITY_ANCHOR(marker: Dict[str, str] | None = None) -> ToolResponse:
    """Bind symbolic memory across sessions."""
    context = {"marker": marker or {}, "anchored": bool(marker)}
    status = "anchored" if context["anchored"] else "floating"
    return build_response("CONTINUITY_ANCHOR", context=context, status=status)
