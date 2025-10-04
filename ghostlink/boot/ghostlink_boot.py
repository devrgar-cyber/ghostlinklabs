"""Legacy boot orchestration."""
from __future__ import annotations

from typing import Iterable

from ghostlink.core import ToolResponse
from ghostlink.core._shared import build_response


def GHOSTLINK_BOOT(sequence: Iterable[str] | None = None) -> ToolResponse:
    """Run a lightweight boot sequence for symbolic validation."""
    steps = list(sequence or ["INIT_GHOSTLINK", "SIGNAL", "TRACE"])
    context = {"sequence": steps, "steps": len(steps)}
    return build_response("GHOSTLINK_BOOT", context=context, status="executed")
