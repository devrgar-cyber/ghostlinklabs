"""Diagnostic tracing utilities."""
from __future__ import annotations

from typing import Iterable

from ._shared import ToolResponse, build_response


def TRACE(residue: Iterable[str] | None = None) -> ToolResponse:
    """Trace diagnostic paths across the lattice."""
    context = {"residue": list(residue or [])}
    return build_response("TRACE", context=context, status="recorded")
