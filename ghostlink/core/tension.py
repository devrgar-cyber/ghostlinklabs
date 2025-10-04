"""Symbolic tension calculator."""
from __future__ import annotations

from typing import Mapping

from ._shared import ToolResponse, build_response


def TENSION(vector: Mapping[str, float] | None = None) -> ToolResponse:
    """Compute differentials between symbolic states."""
    entries = dict(vector or {})
    context = {
        "vector": entries,
        "magnitude": sum(abs(value) for value in entries.values()),
    }
    return build_response("TENSION", context=context, status="balanced")
