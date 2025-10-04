"""Gap detection tooling."""
from __future__ import annotations

from typing import Iterable, List

from ._shared import ToolResponse, build_response


def GAPS(sequence: Iterable[str] | None = None) -> ToolResponse:
    """Identify voids in the symbolic lattice."""
    entries: List[str | None] = list(sequence or [])
    missing = [slot for slot in entries if slot is None]
    context = {"sequence": entries, "voids": missing}
    return build_response("GAPS", context=context, status="mapped")
