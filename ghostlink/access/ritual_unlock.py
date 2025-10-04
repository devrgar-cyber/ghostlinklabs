"""Permission layer rituals."""
from __future__ import annotations

from typing import Dict

from ghostlink.core import ToolResponse
from ghostlink.core._shared import build_response


def RITUAL_UNLOCK(ritual: Dict[str, str] | None = None) -> ToolResponse:
    """Gate manual permission flows."""
    context = {"ritual": ritual or {}, "complete": bool(ritual)}
    status = "open" if context["complete"] else "sealed"
    return build_response("RITUAL_UNLOCK", context=context, status=status)
