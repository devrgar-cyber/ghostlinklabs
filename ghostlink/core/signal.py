"""Origin signal tooling for the GhostLink kernel."""
from __future__ import annotations

from typing import Any, Dict, Optional

from ._shared import ToolResponse, build_response


DEFAULT_SIGNATURE = {
    "frequency": "sovereign",
    "amplitude": 1.0,
    "channel": "symbolic",
}


def SIGNAL(payload: Optional[Dict[str, Any]] = None) -> ToolResponse:
    """Emit the primary broadcast signal for the symbolic lattice.

    Parameters
    ----------
    payload:
        Optional caller supplied data that is merged into the default
        broadcast signature.  Callers can specify additional metadata such as
        the initiating operator or execution intent.
    """
    context = dict(DEFAULT_SIGNATURE)
    if payload:
        context.update(payload)
    return build_response("SIGNAL", context=context, status="broadcast")
