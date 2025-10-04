"""Ritual memory compression logic."""
from __future__ import annotations

from typing import Sequence

from ghostlink.core import ToolResponse
from ghostlink.core._shared import build_response


def COMPRESSION_LOGIC(patterns: Sequence[str] | None = None) -> ToolResponse:
    """Compress sequences into symbolic fragments."""
    entries = list(patterns or [])
    unique = len(set(entries))
    baseline = len(entries) or 1
    context = {
        "patterns": entries,
        "unique": unique,
        "compression_ratio": unique / baseline,
    }
    return build_response("COMPRESSION_LOGIC", context=context, status="compressed")
