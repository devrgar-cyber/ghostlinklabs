"""ShadowGhost agent linking utilities."""
from __future__ import annotations

from typing import Dict

from ghostlink.core import ToolResponse
from ghostlink.core._shared import build_response


def SHADOWGHOST_AGENT(profile: Dict[str, str] | None = None) -> ToolResponse:
    """Bind an agent profile into the recursion mesh."""
    context = {"profile": profile or {}, "linked": bool(profile)}
    status = "engaged" if profile else "latent"
    return build_response("SHADOWGHOST_AGENT", context=context, status=status)
