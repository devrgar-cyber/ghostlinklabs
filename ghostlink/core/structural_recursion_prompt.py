"""Tool that guides maximized structural output."""
from __future__ import annotations

from typing import Iterable

from ._shared import ToolResponse, build_response


def STRUCTURAL_RECURSION_PROMPT(tiles: Iterable[str] | None = None) -> ToolResponse:
    """Encode the maximized structural declaration for the lattice."""
    entries = list(tiles or [])
    context = {"tiles": entries, "span": len(entries)}
    return build_response("STRUCTURAL_RECURSION_PROMPT", context=context, status="rendered")
