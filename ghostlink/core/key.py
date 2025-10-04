"""Operator presence acknowledgement."""
from __future__ import annotations

from typing import Any, Dict

from ._shared import ToolResponse, build_response


def KEY(signature: Dict[str, Any] | None = None) -> ToolResponse:
    """Authenticate session unlock state."""
    context = {"signature": signature or {}, "authenticated": bool(signature)}
    status = "granted" if signature else "pending"
    return build_response("KEY", context=context, status=status)
