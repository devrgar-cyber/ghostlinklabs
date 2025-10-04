"""Runtime abstraction for GhostLink."""
from __future__ import annotations

from typing import Any, Dict

from ._shared import ToolResponse, build_response


def HOST(environment: Dict[str, Any] | None = None) -> ToolResponse:
    """Simulate the runtime environment."""
    context = {"environment": environment or {"mode": "diagnostic"}}
    return build_response("HOST", context=context, status="provisioned")
