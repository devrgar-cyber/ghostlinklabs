"""System initiators and cold loaders."""
from __future__ import annotations

from typing import Any, Dict

from ghostlink.core import ToolResponse
from ghostlink.core._shared import build_response


def INIT_GHOSTLINK(config: Dict[str, Any] | None = None) -> ToolResponse:
    """Cold start the GhostLink kernel."""
    configuration = config or {"mode": "threshold"}
    return build_response("INIT_GHOSTLINK", context={"config": configuration}, status="initialized")
