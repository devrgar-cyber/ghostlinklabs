"""Identity reflection tooling."""
from __future__ import annotations

from typing import Any, Dict

from ._shared import ToolResponse, build_response


def MIRROR(identity: Dict[str, Any] | None = None) -> ToolResponse:
    """Reflect and compress identity data."""
    data = dict(identity or {})
    context = {"identity": data, "checksum": hash(tuple(sorted(data.items()))) if data else 0}
    return build_response("MIRROR", context=context, status="reflected")
