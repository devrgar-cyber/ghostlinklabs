"""Subjective trace harness utilities."""
from __future__ import annotations

from typing import Dict

from ghostlink.core import ToolResponse
from ghostlink.core._shared import build_response


def SUBJECTIVE_TRACE_HARNESS(bias_map: Dict[str, float] | None = None) -> ToolResponse:
    """Capture session bias introduced by operator awareness."""
    context = {"bias": bias_map or {}, "intensity": sum((bias_map or {}).values())}
    return build_response("SUBJECTIVE_TRACE_HARNESS", context=context, status="captured")
